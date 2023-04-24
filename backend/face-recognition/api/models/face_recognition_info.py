from typing import Optional, List
from base.schema import PaginationInfo
from base.models import BaseModel


class FaceRecognitionInfo(BaseModel):
    username: Optional[str]
    hash_username: Optional[str]
    len_embs: Optional[int] = 0
    url: Optional[str]


class FaceRecognitionInfoListOut(PaginationInfo):
    list: List[FaceRecognitionInfo]
