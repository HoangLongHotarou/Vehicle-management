from bson import ObjectId
from pydantic import BaseConfig
from pydantic import BaseModel as BaseModelConfig


class BaseModel(BaseModelConfig):
    class Config(BaseConfig):
        json_encoders = {ObjectId: str}
        allow_population_by_alias = True
        allow_population_by_field_name = True
        arbitrary_types_allowed = True