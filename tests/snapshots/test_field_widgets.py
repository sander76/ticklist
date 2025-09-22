import pytest
from pydantic import BaseModel, ConfigDict

from tests.app_with_form import MyApp


@pytest.mark.parametrize("annotated_type", [str, int, bool])
def test_widgets(annotated_type, snap_compare):
    class MyModel(BaseModel):
        my_value: annotated_type

    app = MyApp(MyModel)
    assert snap_compare(app)


def test_docstrings(snap_compare):
    class MyModel(BaseModel):
        """This is my testing model."""

        model_config = ConfigDict(use_attribute_docstrings=True)

        my_value: str
        """My own little value"""

        other_value: int
        """Another value
        
        With some *markup*
        """

    app = MyApp(MyModel)
    assert snap_compare(app)
