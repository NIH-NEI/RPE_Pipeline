@echo off
set PYTHONPATH=%~dp0RPE_Segmentation;%~dp0RPEOrganelle_Segmenter;%~dp0SegmentationAnalyzer
set PATH=%~dp0python3;%~dp0python3\Library\bin;%PATH%
%~dp0python3\python.exe %*
