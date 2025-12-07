from typing import List
from pydantic import BaseModel


class TechniqueCategory(BaseModel):
    category_name: str
    techniques: List[str]

class ResultExtracted(BaseModel):
    categories: List[TechniqueCategory]