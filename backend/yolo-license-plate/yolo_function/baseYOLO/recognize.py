import re

import cv2
import torch
from yolo_function.baseYOLO.yolo import BaseLicensePlateYOLO


class BaseRecognize(BaseLicensePlateYOLO):
    def __init__(self, yolo_version, pt_file):
        super().__init__(yolo_version, pt_file)

    def convertAlpha(self,i):
            if i <= 9: return f'{i}'
            return chr(i+55)

    def predict(self,LpRegion):
        segment = self.model(LpRegion)
        coordinates_matrix = segment.xyxy[0]
        if coordinates_matrix == [] or coordinates_matrix == None: return None
        untrack = []
        for coordinates in coordinates_matrix:
            untrack.append(float(coordinates[1]))
        if untrack==[]:return None
        track = min(untrack)
        above = {}
        under = {}
        for coordinates in coordinates_matrix:
            if float(coordinates[4]<0.5): continue
            if abs(coordinates[1]-track) < 12:
                above[coordinates[0]] = (float(coordinates[4]),int(coordinates[5]))
            else:
                under[coordinates[0]] = (float(coordinates[4]),int(coordinates[5]))
        plate = ""
        for i in sorted(above.keys()):
            label = self.convertAlpha(above[i][1])
            if under == {} and above[i][1] > 9:
                plate = plate.replace('-', '')
                label += '-'
            plate += label
        if under != {}:
            plate += "-"
            for i in sorted(under.keys()):
                plate += self.convertAlpha(under[i][1])
        return plate if re.match("[0-9]{2}[A-Z]{1}(|[0-9]{1}|[A-Z]{1})-[0-9]{4,5}",plate) else None