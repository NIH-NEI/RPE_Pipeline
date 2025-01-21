import torch
from mrcnn_torch.mrcnn_model import build_model

device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')
model = build_model(
    num_classes=2,
    detections_per_img=100,
    score_thresh=0.5)
