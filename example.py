from datetime import datetime
from typing import Annotated

from pydantic import BaseModel
from textual.app import App

from ticklist.form import Form
from ticklist.tick_annotations import Multiline
from ticklist.types import NO_VALUE


class Person(BaseModel):
    """Define a form using a pydantic model."""

    name: str
    """Name of the person."""

    age: int = 10
    notes: Annotated[str, Multiline()]
    date_of_birth: datetime


class MyApp(App[None]):
    def on_mount(self) -> None:
        def handle_form_result(result: Person | None) -> None:
            self.exit(message=f"{result=!r}")

        frm = Form(Person, NO_VALUE)
        self.push_screen(frm, handle_form_result)


if __name__ == "__main__":
    MyApp().run()
