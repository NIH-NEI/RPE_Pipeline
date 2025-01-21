import os, sys
import datetime

CODEBASE = os.path.dirname(os.path.abspath(__file__))
_cdir = CODEBASE
_orgs = _refs = _ana = False
for i in range(2):
    if not _refs:
        testpath = os.path.join(_cdir, 'RPE_Segmentation', 'predict.py')
        if os.path.isfile(testpath):
            pythondir = os.path.join(_cdir, 'RPE_Segmentation')
            if not pythondir in sys.path:
                sys.path.insert(0, pythondir)
            _refs = True
    if not _ana:
        testpath = os.path.join(_cdir, 'SegmentationAnalyzer', 'GenerateShapeMetricsBatch.py')
        if os.path.isfile(testpath):
            pythondir = os.path.join(_cdir, 'SegmentationAnalyzer')
            if not pythondir in sys.path:
                sys.path.insert(0, pythondir)
            _ana = True
    if not _orgs:
        testpath = os.path.join(_cdir, 'RPEOrganelle_Segmenter', 'gfpsegment.py')
        if os.path.isfile(testpath):
            pythondir = os.path.join(_cdir, 'RPEOrganelle_Segmenter')
            if not pythondir in sys.path:
                sys.path.insert(0, pythondir)
            _orgs = True
    _cdir = os.path.dirname(_cdir)
del _cdir, _refs, _orgs, _ana

from src2ome import GFP_MAP, iter_stacks, create_ome_stacks

import predict
import gfpsegment
import GenerateShapeMetricsBatch

def _iter_organelles(srcdir):
    for fn in os.listdir(srcdir):
        sdir = os.path.join(srcdir, fn)
        if not os.path.isdir(sdir): continue
        gfp = fn.lower()
        if not gfp in GFP_MAP:
            print(f'Unknown GFP: "{gfp}" -- skipped.')
            continue
        yield GFP_MAP[gfp]
        
def segment_actindna(basedir, srcdir, tgtdir):
    print(f'Segmenting Actin and DNA of .ome.tif stacks in "{srcdir}", results in "{tgtdir}" ...')
    start_ts = datetime.datetime.now()
    nstacks = 0
    for gfp in _iter_organelles(srcdir):
        gfpdir = os.path.join(srcdir, gfp.dirname)
        tifdir = os.path.join(tgtdir, gfp.dirname, 'Cell')
        csvdir = os.path.join(tifdir, 'csv')
        os.makedirs(csvdir, exist_ok=True)
        assert os.path.isdir(csvdir), f'Could not create directory "{csvdir}"'
        args = ['--data-dir', basedir, '--prediction-dir', tifdir, '--csv-dir', csvdir, 'All']
        print('predict.py', ' '.join(args), '<OME_TIFF_List>')
        print('=====')
        stklist = []
        for stkpath in iter_stacks(gfpdir):
            stklist.append(stkpath)
            nstacks += 1
            if len(stklist) >= 16:
                print((args+stklist))
                predict.main(args+stklist)
                stklist = []
        if len(stklist) > 0:
            predict.main(args+stklist)
    elapsed = datetime.datetime.now() - start_ts
    print(f'Segmenting Actin and DNA of {nstacks} stack(s) done in {str(elapsed)}')

def segment_gfps(srcdir, tgtdir):
    print(f'Segmenting GFPs of .ome.tif stacks in "{srcdir}", results in "{tgtdir}" ...')
    start_ts = datetime.datetime.now()
    for gfp in _iter_organelles(srcdir):
        stkdir = os.path.join(srcdir, gfp.dirname)
        savedir = os.path.join(tgtdir, gfp.dirname)
        os.makedirs(savedir, exist_ok=True)
        arglist = ['--channelname', gfp.id, '--path_stackfolders', stkdir, '--savedir', savedir]
        print('gfpsegment.py', ' '.join(arglist))
        print('=====')
        gfpsegment.main(arglist)
    elapsed = datetime.datetime.now() - start_ts
    print(f'Segmenting GFPs done in {str(elapsed)}')
    
def segment_analysis(srcdir, tgtdir):
    print(f'Analyzing segmentations in "{srcdir}", results in "{tgtdir}" ...')
    start_ts = datetime.datetime.now()
    for gfp in _iter_organelles(srcdir):
        channel = gfp.dirname
        gfpfolder = os.path.join(srcdir, gfp.dirname)
        cellfolder = os.path.join(srcdir, gfp.dirname, 'Cell', 'csv')
        savedir = os.path.join(tgtdir, gfp.dirname, 'calcs')
        os.makedirs(savedir, exist_ok=True)
        usedna = channel == 'FBL'
        print('GenerateShapeMetricsBatch.py', '--GFPFolder', gfpfolder, '--CellFolder', cellfolder,
              '--savepath', savedir, '--channel', channel, '--usednareference', usedna)
        print('=====')
        GenerateShapeMetricsBatch.calculateCellMetricsAPI(gfpfolder, cellfolder, savedir, channel,
                         False, False, False, False, False,
                         usedna, selected_dilation=2, num_processes=4)
    elapsed = datetime.datetime.now() - start_ts
    print(f'Analyzing segmentations done in {str(elapsed)}')

if __name__ == '__main__':
    
    if len(sys.argv) < 2:
        print('Please specify RPE Map Data Root directory in the command line.')
        print('It must contain "model_weights" and either "SourceData" or "StackData".')
        sys.exit(1)

    start_ts = datetime.datetime.now()
    basedir = sys.argv[1]

    # Step 1. Convert source image files into .ome.tif stacks.
    tgtdir = os.path.join(basedir, 'StackData')
    for fp in iter_stacks(tgtdir):
        # If '.../StackData' already exists, skip step 1
        break
    else:
        srcdir = os.path.join(basedir, 'SourceData')
        assert os.path.isdir(srcdir), f'Directory "{srcdir}" must exist.'
        os.makedirs(tgtdir, exist_ok=True)
        assert os.path.isdir(tgtdir), f'Could not create directory "{tgtdir}"'
        #
        create_ome_stacks(srcdir, tgtdir)
        print('', flush=True)
    #
    
    # Step 2. Segment reference channels (Actin and DNA).
    srcdir = os.path.join(basedir, 'StackData')
    assert os.path.isdir(srcdir), f'Directory "{srcdir}" must exist.'
    tgtdir = os.path.join(basedir, 'Results', 'final_segmentations')
    os.makedirs(tgtdir, exist_ok=True)
    assert os.path.isdir(tgtdir), f'Could not create directory "{tgtdir}"'
    segment_actindna(basedir, srcdir, tgtdir)
    print('', flush=True)

    # Step 3. Segment GFP channels.
    segment_gfps(srcdir, tgtdir)
    print('', flush=True)

    # Step 4. Perfortm segmentation analysis.
    srcdir = tgtdir
    tgtdir = os.path.join(basedir, 'Results', 'Analysis')
    os.makedirs(tgtdir, exist_ok=True)
    assert os.path.isdir(tgtdir), f'Could not create directory "{tgtdir}"'
    segment_analysis(srcdir, tgtdir)
    print('', flush=True)

    elapsed = datetime.datetime.now() - start_ts
    print(f'All done in {str(elapsed)}; exiting(0).')
    sys.exit(0)


