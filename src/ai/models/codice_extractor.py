from typing import List, Literal
from pydantic import BaseModel


class Licence(BaseModel):
    licence_name: Literal["Psionica (P)", "Temporale (t)", "Gravitazionale (G)", "Antimateria (e+)", "Magnetica (Mx)", "Quantistica (Q)", "Luce (c)", "Livello di Sviluppo Tecnologico (LTK)"]
    licence_level: int

class Technique(BaseModel):
    technique_name: str
    licences: List[Licence]

class TechniqueCategory(BaseModel):
    category_name: str
    techniques: List[Technique]

class ResultExtracted(BaseModel):
    categories: List[TechniqueCategory]