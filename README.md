# RPE_Pipeline

Python-based software suite for running Segmentation and Analysis of biological images
as part of the RPE Map project.

## Contributors

*Andrei Volkov (NEI/NIH via Guidehouse), Pushkar Sathe (NEI/NIH), Nicholas Schaub
(National Center for the Advancement of Translational Science).*

## System Requirements

- Operating Systems: Windows 10 or 11 or Linux (Ubuntu, Fedora, etc.) It might also work on MacOS,
though it has not been tested.
- 16 GB RAM or more
- 20GB disk space for the code plus ~1 GB per image stack of shape (4,27,1278,1078).
- CUDA-enabled GPU w. at least 8GB RAM (optional)

## Setting Up Development Environment

Typical installation time: 10-20 min.

1. Download and install [Git](https://git-scm.com/downloads) for your platform.
On Windows or MacOS systems, download and install C++ build tools.
On MacOS it's XCode, on Windows, either Microsoft Visual C++ or MinGW.
When installing MSVC, make sure you have checked the box for x64/x86 build tools,
such as `MSVC v143 - VS 2022 C++ x64/x86 build tools (latest)`.

2. Download and install [Miniconda](https://docs.conda.io/en/latest/miniconda.html)
or [Anaconda](https://www.anaconda.com/products/individual).

3. Check out **RPE_Pipeline** to a local directory, such as `C:\RpeMap\RPE_Pipeline`.
The git command is like this:

	`git clone https://github.com/NIH-NEI/RPE_Pipeline.git C:\RpeMap\RPE_Pipeline\`

4. Check out the following RPE Map repositories to directories inside the RPE_Pipeline:
[RPE_Segmentation](https://github.com/NIH-NEI/RPE_Segmentation),
[RPEOrganelle_Segmenter](https://github.com/NIH-NEI/RPEOrganelle_Segmenter) and
[SegmentationAnalyzer](https://github.com/NIH-NEI/SegmentationAnalyzer).
The git commands are:

```
  git clone https://github.com/NIH-NEI/RPE_Segmentation.git C:\RpeMap\RPE_Pipeline\RPE_Segmentation\
  git clone https://github.com/NIH-NEI/RPEOrganelle_Segmenter.git C:\RpeMap\RPE_Pipeline\RPEOrganelle_Segmenter\
  git clone https://github.com/NIH-NEI/SegmentationAnalyzer.git C:\RpeMap\RPE_Pipeline\SegmentationAnalyzer\
```

5. Run Anaconda Prompt (or Terminal), cd to `C:\RpeMap\RPE_Pipeline`.

6. Create Conda Virtual Environment (do this once on the first run):

	`conda env create --file conda-environment.yml`
   
7. Activate the Virtual Environment:

	`conda activate RPE_Map`
	
8. Install extra packages (do this once on the first run):

	`pip install -r x-requirements.txt`

9. To run the pipeline, prepare the data directory (as described below), cd to `C:\RpeMap\RPE_Pipeline`,
activate the VE and type:

	`python pipeline.py /your/data/directory`

Results will be stored in `/your/data/directory/Results`.

To delete the Virtual environment at the Conda prompt, deactivate it first, if it is active:

`conda deactivate`

then type:

`conda remove --name RPE_Map`


## Preparing Data Directory
	
Create a local directory for RPE Map Data, such as `C:\RpeMap\DataRoot`, place inside it
the pre-trained Mask-RCNN model weights (`C:\RpeMap\DataRoot\model_weights\*.pth`) and source data.
Ther source data (RPE Map image stacks) can be either in the form of .ome.tif stacks (`C:\RpeMap\DataRoot\StackData\<org>\<week>\*.ome.tif`) or individual .tif files (one per channel/frame), named according to the RPE Map naming conventions
(`C:\RpeMap\DataRoot\SourceData\<org>\<week>\*.tif`). In the latter case, these  individual files will be converted
to .ome.tif stacks before processing by the RPE pipeline.

The resulting directory tree must look like  this:

```
C:\RpeMap\DataRoot\
├───model_weights
│       Mask_RCNN-Actin-RGB-0050.pth
│       Mask_RCNN-DNA-BW-0050.pth
│
└───SourceData
    ├───FBL
    │   ├───P3-W2-FBL
    │   │       DAO-190426-60X-FBL-W2.mes
    │   │       P3-W2-FBL_G03_T0001F002L01A01Z01C02.tif
    │   │       P3-W2-FBL_G03_T0001F002L01A01Z01C04.tif
    │   │       .....
    ├───Sec61
    │   ├───P1-W2-SEC
    │   │       006_DAO-180102-60X-SEC-W2.mes
    │   │       MeasurementDetail.mrf
    │   │       P1-W2-SEC_G02_T0001F004L01A01Z01C02.tif
    │   │       P1-W2-SEC_G02_T0001F004L01A01Z01C04.tif
    │   │       .....
```

Or like this:

```
C:\RpeMap\DataRoot\
├───model_weights
│       Mask_RCNN-Actin-RGB-0050.pth
│       Mask_RCNN-DNA-BW-0050.pth
│
└───StackData
    ├───FBL
    │   ├───P1-W2-FBL
    │   │       P1-W2-FBL_G03_F002.ome.tif
    │   │       P1-W2-FBL_G05_F001.ome.tif
    │   │       P1-W2-FBL_G07_F004.ome.tif
    │   │       P1-W2-FBL_G11_F002.ome.tif
    │   │
    │   ....................
    ├───Sec61
    │   ├───P1-W2-SEC
    │   │       P1-W2-SEC_G02_F004.ome.tif
    │   │       P1-W2-SEC_G03_F003.ome.tif
    │   │       P1-W2-SEC_G08_F002.ome.tif
    │   │       P1-W2-SEC_G10_F004.ome.tif
    │   │
    │   .....................
```

## Running Test/Demo from the Development Environment

Unzip `RpeMapDemoData.zip` into a local directory (on Windows machines, right-click on the .zip and select "Extract all..."
into the directory `C:\RpeMap`). It will create the `DataRoot` directory inside, which is
structured as described above. After that, cd to `C:\RpeMap\RPE_Pipeline`, activate the **RPE_Map** VE and type:

`python pipeline.py C:\RpeMap\DataRoot`

The whole process will take about 3-5 hours on a typical system with GPU:
Segmenting Actin/DNA - 35-40m (1m30s-1m40s per stack),
Segmenting organelles - 10m (30s per stack),
Segmentation Analysis - 3h30m to 4h (12-15m per stack).
The results can be found in `C:\RpeMap\DataRoot\Results`.

## Running RPE_Pipeline from the Windows pre-built distribution package

An RPE_Pipeline distribution package `RPE_Pipeline-Win64.zip` for Win64 systems is available upon request.
It contains everything needed for running the pipeline, so you are spared from installing pre-requisites - conda, git, built tools, etc.
Just right-click on it, "Extract all..." to `C:\RpeMap`, then do the same for `RpeMapDemoData.zip`
(see [Running Test/Demo](#running-rpe_pipeline-from-the-windows-pre-built-distribution-package)), open "Command Prompt",
cd to `C:\RpeMap\RPE_Pipeline` and type the command:

`rpemap.bat pipeline.py C:\RpeMap\DataRoot`

You can also run any other scripts from RPE Map packages
[RPE_Segmentation](https://github.com/NIH-NEI/RPE_Segmentation/),
[RPEOrganelle_Segmenter](https://github.com/NIH-NEI/RPEOrganelle_Segmenter) and
[SegmentationAnalyzer](https://github.com/NiH-NEI/SegmentationAnalyzer), for example:

- To run the Mask_RCNN training script, extract `RpeMapTrainingData.zip` into `C:\RpeMap` and type:

	`rpemap.bat RPE_Segmentation\train.py -d C:\RpeMap\DataRoot DNA`
	
	`rpemap.bat RPE_Segmentation\train.py -d C:\RpeMap\DataRoot Actin`

- To run the evaluation script, extract [Test_Data.zip](https://github.com/NIH-NEI/RPE_Segmentation/releases/download/testdata/Test_Data.zip)
into `C:\RpeMap\DataRoot` and type:

	`rpemap.bat RPE_Segmentation\evaluate.py C:\RpeMap\DataRoot\Test_data -f`

The following examples are basically individual steps of *RPE_Pipeline* and assume that you have extracted
`RpeMapDemoData.zip` into `C:\RpeMap` (see [Running Test/Demo](#running-testdemo-from-the-development-environment)).

- To convert raw data into .ome.tif stacks:

	`rpemap.bat src2ome.py C:\RpeMap\DataRoot\SourceData C:\RpeMap\DataRoot\StackData`

- To run the segmentation of reference channels (Actin and DNA) of the Sec61 stacks, type:

	`rpemap.bat RPE_Segmentation\predict.py --data-dir C:\RpeMap\DataRoot --prediction-dir C:\RpeMap\DataRoot\Results\final_segmentations\SEC\Cell --csv-dir C:\RpeMap\DataRoot\Results\final_segmentations\SEC\Cell\csv All C:\RpeMap\DataRoot\StackData\SEC`

- To run the segmentation of an organelle channel (Sec61 in this case), make sure
the `C:\RpeMap\DataRoot\Results\final_segmentations\Sec61` directory exists, and type:

	`rpemap.bat RPEOrganelle_Segmenter\gfpsegment.py --channelname sec61b --path_stackfolders C:\RpeMap\DataRoot\StackData\Sec61 --savedir C:\RpeMap\DataRoot\Results\final_segmentations\Sec61`

- To run the segmentation analysis of an organelle (Sec61), create directory `\RpeMap\DataRoot\Results\Analysis\Sec61\calcs`
and type:

	`rpemap.bat SegmentationAnalyzer\GenerateShapeMetricsBatch.py --GFPFolder C:\RpeMap\DataRoot\Results\final_segmentations\Sec61 --CellFolder C:\RpeMap\DataRoot\Results\final_segmentations\Sec61\Cell\csv --savepath C:\RpeMap\DataRoot\Results\Analysis\Sec61\calcs --channel Sec61 --usednareference False`
	
## Running RPE_Pipeline as Docker container

If you have a system with [Docker](https://docs.docker.com/get-started/get-docker/) installed, you can build
a containerized version of RPE_Pipeline. In this case you won't need any pre-requisites (conda, git, build tools, etc.),
since all the building will be done by Docker inside the container. All you have to do is to check out *RPE_Pipeline*
or download .zip from the GitHub and expand it into a local directory. No need to check out dependent repositories
(*RPE_Segmentation*, etc.) either. To build the container, open terminal (or Command Prompt), cd to the RPE_Pipeline directory
(where `Dockerfile` is located) and type:

`docker build -t rpemappipeline .`

The build process normally takes about 10 minutes. To run *RPE_Pipeline* from the container, prepare the data by unzipping
`RpeMapDemoData.zip` into `C:\RpeMap` and type the docker command:

`docker run --shm-size="4g" -it --gpus=all --name=rpemapall --rm --mount type=bind,source=C:\RpeMap\DataRoot,destination=/RpeMapData rpemappipeline pipeline.py /RpeMapData`

You can run any other scripts from RPE Map container. Check example commands in the previous section
and modify them in the following way:

- Replace `rpemap.bat` with `docker run --shm-size="4g" -it --gpus=all --name=rpemapall --rm --mount type=bind,source=C:\RpeMap\DataRoot,destination=/RpeMapData rpemappipeline`

- Replace `C:\RpeMap\DataRoot` with `/RpeMapData` (this is how it is mounted inside the container)

- Replace all backslashes `\` with forward slashes `/`

For example, to train Mask_RCNN to segment the DNA channel, type the command:

`docker run --shm-size="4g" -it --gpus=all --name=rpemapall --rm --mount type=bind,source=C:\RpeMap\DataRoot,destination=/RpeMapData rpemappipeline RPE_Segmentation/train.py DNA -d /RpeMapData`

