from typing import Collection, Type

from pydantic import BaseModel
from textual.app import App
from ticklist import form
from ticklist.annotation_iterators import ANNOTATION_ITERATORS
from ticklist.types import NO_VALUE, AnnotationIterator


class MyApp(App):
    """An app for testing purposes."""

    CSS_PATH = "app_with_form.tcss"

    def __init__(
        self,
        model: Type[BaseModel],
        value: BaseModel | None = None,
        annotation_iterators: Collection[AnnotationIterator] | None = None,
    ):
        self._model = model
        self._value = value if value else NO_VALUE

        self._annotation_iterators = (
            annotation_iterators if annotation_iterators else ANNOTATION_ITERATORS
        )
        super().__init__()

    def on_mount(self):
        self.push_screen(
            form.Form(self._model, self._value, self._annotation_iterators)
        )
