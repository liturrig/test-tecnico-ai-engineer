from typing import Literal
from pydantic import BaseModel

class ClassificationResult(BaseModel):
    menu_classification: Literal["structured", "unstructured"]