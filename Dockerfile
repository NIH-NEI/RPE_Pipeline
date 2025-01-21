FROM python:3.12-slim

WORKDIR /RPE_Pipeline

COPY *.py ./
COPY *.txt ./

RUN DEBIAN_FRONTEND=noninteractive \
  apt-get update \
  && apt-get install -y git \
  && apt-get install -y build-essential \
  && rm -rf /var/lib/apt/lists/*

RUN git clone https://github.com/NIH-NEI/RPE_Segmentation.git ./RPE_Segmentation/
RUN git clone https://github.com/NIH-NEI/RPEOrganelle_Segmenter.git ./RPEOrganelle_Segmenter/
RUN git clone https://github.com/NIH-NEI/SegmentationAnalyzer.git ./SegmentationAnalyzer/
ENV PYTHONPATH=/RPE_Pipeline:/RPE_Pipeline/RPE_Segmentation:/RPE_Pipeline/RPEOrganelle_Segmenter:/RPE_Pipeline/SegmentationAnalyzer

RUN pip install --root-user-action ignore --upgrade pip setuptools wheel
RUN pip install --root-user-action ignore -r requirements.txt
RUN pip install --root-user-action ignore -r x-requirements.txt
RUN pip cache purge
RUN python initmodel.py

ENTRYPOINT [ "python" ]
