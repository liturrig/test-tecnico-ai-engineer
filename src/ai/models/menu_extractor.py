from typing import List, Literal
from pydantic import BaseModel


class Skill(BaseModel):
    skill_name: Literal["Psionica (P)", "Temporale (t)", "Gravitazionale (G)", "Antimateria (e+)", "Magnetica (Mx)", "Quantistica (Q)", "Luce (c)", "Livello di Sviluppo Tecnologico (LTK)"]
    skill_level: int

class Dish(BaseModel):
    dish_name: str
    ingredients: List[str]
    techniques: List[str]

class Restaurant(BaseModel):
    planet_name: Literal["Pandora", "Tatooine", "Cybertron", "Ego", "Asgard", "Krypton", "Arrakis", "Namecc", "Klyntar"]
    restaurant_name: str
    chef_name: str
    skills: List[Skill]
    dishes: List[Dish]