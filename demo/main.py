from typing import Type

from textual import on
from textual.app import App, ComposeResult
from textual.widgets import Button
from ticklist import form
from ticklist.annotation_iterators import ANNOTATION_ITERATORS
from ticklist.types import NO_VALUE

from demo.models import MyCar


class MyApp(App):
    """An app for testing purposes."""

    # CSS_PATH = "app_with_form.tcss"

    def compose(self) -> ComposeResult:
        yield Button("order", id="order_a_car")

    @on(Button.Pressed, "#order_a_car")
    def _order_car(self):
        self.app.push_screen(
            form.Form(
                MyCar, instance=NO_VALUE, annotation_iterators=ANNOTATION_ITERATORS
            )
        )


if __name__ == "__main__":
    print("running")
    app = MyApp()
    app.run()
