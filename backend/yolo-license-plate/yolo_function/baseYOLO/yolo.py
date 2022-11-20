import re

import cv2
import imutils
import matplotlib.pyplot as plt
import torch


class BaseLicensePlateYOLO:
    def __init__(self, yolo_version, pt_file):
        # self.model = torch.hub.load(
        #     yolo_version,
        #     'custom',
        #     pt_file,
        #     source='local'
        # )
        self.model = torch.hub.load(
            yolo_version,
            'custom',
            pt_file,
        )

