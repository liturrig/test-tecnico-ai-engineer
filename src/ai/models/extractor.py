from typing import List
from pydantic import BaseModel


class Skill(BaseModel):
    skill_name: str
    skill_level: int

class Dish(BaseModel):
    dish_name: str
    ingredients: List[str]
    techniques: List[str]

class Restaurant(BaseModel):
    restaurant_name: str
    chef_name: str
    skills: List[Skill]
    dishes: List[Dish]