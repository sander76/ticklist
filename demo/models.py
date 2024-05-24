from enum import Enum
from typing import Annotated

from pydantic import BaseModel

from ticklist import tick_annotations as ta


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
    customer_name: str

    color: Colors

    edition: (
        Annotated[Normal, ta.Label("normal")] | Annotated[Sports, ta.Label("sports")]
    )

    extra_insurance: bool = True
