from enum import Enum

from pydantic import BaseModel


class Colors(Enum):
    BLUE = "blue"
    RED = "red"
    GREEN = "green"


class InteriorColor(Enum):
    GREY = "grey"
    BLACK = "black"


class Engine(Enum):
    FOUR_CILINDER = "four_cilinder"
    SIX_CILINDER = "six_cilinder"


class Normal(BaseModel):
    interior_color: InteriorColor


class Sports(BaseModel):
    interior_color: InteriorColor
    engine: Engine = Engine.FOUR_CILINDER


class MyCar(BaseModel):
    color: Colors

    edition: Normal | Sports

    extra_insurance: bool = True
