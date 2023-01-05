from ONNXModel.baseONNX.onnxmodels import BaseYOLO
import re

def detection(yolo: BaseYOLO, image):
    for (x0,y0,x1,y1,score,label) in yolo.predict(image):
        if score <= 0.5: continue
        # yield image[y0:y1,x0:x1]
        yield (x0,y0,x1,y1)

def recognize(yolo: BaseYOLO, image):
    coordinates_matrix = []
    for pre in yolo.predict(image):
        coordinates_matrix.append(pre)

    if coordinates_matrix == [] or coordinates_matrix == None: return None
    untrack = []
    for coordinates in coordinates_matrix:
        untrack.append(float(coordinates[1]))
    if untrack==[]:return None
    track = min(untrack)
    above = {}
    under = {}
    for coordinates in coordinates_matrix:
        if float(coordinates[4]<=0.5): return None
        if abs(coordinates[1]-track) < 12:
            above[coordinates[0]] = (float(coordinates[4]),int(coordinates[5]))
        else:
            under[coordinates[0]] = (float(coordinates[4]),int(coordinates[5]))
    plate = ""
    for i in sorted(above.keys()):
        label = convertAlpha(above[i][1])
        if under == {} and above[i][1] > 9:
            plate = plate.replace('-', '')
            label += '-'
        plate += label
    if under != {}:
        plate += "-"
        for i in sorted(under.keys()):
            plate += convertAlpha(under[i][1])
    return plate if re.match("[0-9]{2}[A-Z]{1}(|[0-9]{1}|[A-Z]{1})-[0-9]{4,5}",plate) else None

def convertAlpha(i):
    if i <= 9: return f'{i}'
    return chr(i+55)