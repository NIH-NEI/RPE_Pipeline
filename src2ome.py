import os, sys
import datetime
import glob

from collections import namedtuple

CODEBASE = os.path.dirname(os.path.abspath(__file__))
_cdir = CODEBASE
for i in range(2):
    testpath = os.path.join(_cdir, 'RPEOrganelle_Segmenter', 'gfpsegment.py')
    if os.path.isfile(testpath):
        pythondir = os.path.join(_cdir, 'RPEOrganelle_Segmenter')
        if not pythondir in sys.path:
            sys.path.insert(0, pythondir)
        break
    _cdir = os.path.dirname(_cdir)
del _cdir

from gfpseg.stackio.stack3d import Stack
import gfpseg.stackio.Channel as Channel

gfp_channel_attributes = ['id', 'dirname', 'canonical', 'short']
GfpChannel = namedtuple('GfpChannel', gfp_channel_attributes)

GFP_LIST = [
    GfpChannel('lmnb1', 'LMN', 'LaminB', 'LMN'),
    GfpChannel('lamp1', 'LAMP1', 'LAMP1', 'LAMP1'),
    GfpChannel('sec61b', 'Sec61', 'Sec61b', 'SEC'),
    GfpChannel('st6gal1', 'ST6GAL1', 'ST6GAL1', 'ST6GAL1'),
    GfpChannel('tom20', 'TOM20', 'TOM20', 'TOM'),
    GfpChannel('fbl', 'FBL', 'FBL', 'FBL'),
    GfpChannel('myh10', 'myosin', 'MYH10', 'MYH'),
    GfpChannel('rab5', 'RAB5', 'RAB5', 'RAB5'),
    GfpChannel('tuba1b', 'TUBA', 'TUBA1B', 'TUB'),
    GfpChannel('dsp', 'DSP', 'DSP', 'DSP'),
    GfpChannel('slc25a17', 'SLC', 'SLC25A17', 'SLC'),
    GfpChannel('pxn', 'PXN', 'PXN', 'PXN'),
    GfpChannel('gja1', 'GJA1', 'GJA1', 'GJA1'),
    GfpChannel('ctnnb1', 'CTNNB', 'CTNNB1', 'CTNNB1'),
    GfpChannel('actb', 'ACTB', 'ACTB', 'ACTB'),
    GfpChannel('cetn2', 'CETN2', 'CETN2', 'CETN2'),
    GfpChannel('lc3b', 'LC3B', 'LC3B', 'LC3B'),
    GfpChannel('tjp1', 'ZO1', 'ZO1', 'ZO1'),
]
GFP_MAP = {}
for gfp in GFP_LIST:
    for attr in gfp:
        GFP_MAP[attr.lower()] = gfp

def iter_stacks(gfpdir):
    for fpath in glob.iglob('**/*.ome.tif', root_dir=gfpdir, recursive=True):
        yield os.path.join(gfpdir, fpath)

def create_ome_stacks(srcdir, tgtdir):
    print(f'Reading source data from {srcdir}, creating OME TIFF stacks in {tgtdir} ...')
    start_ts = datetime.datetime.now()
    for _fpath in glob.iglob('**/*.mes', root_dir=srcdir, recursive=True):
        fpath = os.path.join(srcdir, _fpath)
        filedir, filename = os.path.split(fpath)
        basename,  ext = os.path.splitext(filename)
        parts = basename.split('-')
        if len(parts) < 2: continue
        _gfp = parts[-2]
        gfp = _gfp.lower()
        if not gfp in GFP_MAP:
            print(f'Unknown GFP: {gfp} -- skipped.')
            continue
        gfp = GFP_MAP[gfp]
        savepath = os.path.join(tgtdir, gfp.dirname)
        os.makedirs(savepath,  exist_ok=True)
        s = Stack(alphabet=Channel.channel.getrepalphabet(channelname=gfp.id))
        s.generatestacksfromdirs(filepath=os.path.join(srcdir, gfp.dirname), savepath=savepath)
    elapsed = datetime.datetime.now() - start_ts
    print('Generating OME TIFF stacks done in:', str(elapsed))

if __name__ == '__main__':
    
    if len(sys.argv) < 3:
        print('Usage: src2ome.py /path/to/SourceData /path/to/StackData')
        sys.exit(1)

    srcdir = os.path.abspath(sys.argv[1])
    tgtdir = os.path.abspath(sys.argv[2])
    for fp in iter_stacks(tgtdir):
        # If '.../StackData' already exists, skip step 1
        print(f'"{tgtdir}" already contains some .ome.tif files.')
        break
    else:
        assert os.path.isdir(srcdir), f'Directory "{srcdir}" must exist.'
        os.makedirs(tgtdir, exist_ok=True)
        assert os.path.isdir(tgtdir), f'Could not create directory "{tgtdir}"'
        #
        create_ome_stacks(srcdir, tgtdir)
        print('', flush=True)

    sys.exit(0)
