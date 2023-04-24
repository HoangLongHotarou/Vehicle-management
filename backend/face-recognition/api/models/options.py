from base.models import BaseModel
from enum import Enum

class TrainOptions(str,Enum):
    new_train = 'new_train'
    retrain = 'retrain'