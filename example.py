from tkinter.tix import Form

from pydantic import BaseModel
from textual.app import App

from ticklist.annotation_iterators import ANNOTATION_ITERATORS


class MyModel(BaseModel):
    name: str
    age: int


class MyApp(App):
    def on_mount(self) -> None:
        frm = Form(MyModel, None, ANNOTATION_ITERATORS)
        self.push_screen(frm)


if __name__ == "__main__":
    app = MyApp()
    app.run()
