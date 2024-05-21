from enum import Enum
from typing import Literal
from uuid import uuid4

import pytest
from pydantic import BaseModel
from textual.containers import Container
from textual.widgets import Input
from ticklist.form import Form, _Option

from tests.app_with_form import MyApp


class TestModelWithSingularAnnotation:
    """Test class for testing annotations which result in a single input field.

    Examples: int, str.
    """

    class MyStringModel(BaseModel):
        my_value: str

    class MyStringModelWithDefault(BaseModel):
        my_value: str = "my_default"

    class MyIntModel(BaseModel):
        my_value: int

    class MyIntModelWithDefault(BaseModel):
        my_value: int = 999

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "app,result",
        [
            (MyApp(MyStringModel), {}),
            (MyApp(MyStringModelWithDefault), {"my_value": "my_default"}),
            (MyApp(MyIntModel), {}),
            (MyApp(MyIntModelWithDefault), {"my_value": "999"}),
        ],
    )
    async def test_initial_values(self, app, result):
        """Form object has default model value at startup."""

        async with app.run_test():
            my_form = app.query_one(Form)

            assert my_form.obj == result

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "app,manual_input",
        [
            (MyApp(MyStringModel), "custom_string"),
            (MyApp(MyStringModelWithDefault), "custom_string"),
            (MyApp(MyIntModel), "12"),
            (MyApp(MyIntModelWithDefault), "12"),
        ],
    )
    async def test_manual_input(self, app, manual_input):
        """User entry in input ends up in form object."""

        async with app.run_test() as pilot:
            my_form = app.query_one(Form)
            my_inp = app.query_one(Input)

            my_inp.clear()
            my_inp.focus()
            # simulate manual key presses.
            await pilot.press(*list(manual_input))

            assert my_form.obj == {"my_value": manual_input}


def _check_state(option_container: Container, enabled: bool):
    """Check the state of the checkbox and field widget inside the option_container

    helper function.
    """
    field_widget = option_container.query_one("FieldWidget")
    option = option_container.query_one(_Option)

    assert field_widget.disabled is not enabled
    assert option.checked is enabled


async def _click_option_container(option_container: Container, pilot):
    """Make this option container active by clicking the option checkbox.

    helper function.
    """
    option = option_container.query_one(_Option)
    if not option.id:
        option.id = f"custom_id{uuid4()!s}"

    await pilot.click(f"#{option.id}")


class TestSimpleMultipleWidgets:
    """Multiple widgets representing a single pydantic field.

    Using the textual test frame work we create an app with a form
    containing multiple widgets representing a single pydantic field.
    """

    class MyModel(BaseModel):
        """The model which creates multiple field widgets.
        It will create the following form:
        ____________________________________________________
        |                                                    |
        |  my_value:                                         |
        |      [ ] A                                         |
        |      [ ] B                                         |
        |                                                    |
        |                         [ OK ][ CANCEL ]           |
        |____________________________________________________|

        """

        my_value: Literal["A", "B"]

    class MyModelWithDefault(BaseModel):
        """Same as above, but with a default value and using enums."""

        class MyEnum(Enum):
            A = "A"
            B = "B"

        my_value: MyEnum = MyEnum.B

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "app,result,enabled",
        [
            (MyApp(MyModel), {}, (False, False)),
            (
                MyApp(MyModelWithDefault),
                {"my_value": MyModelWithDefault.MyEnum.B},
                (False, True),
            ),
            (
                MyApp(
                    MyModelWithDefault,
                    MyModelWithDefault(my_value=MyModelWithDefault.MyEnum.A),
                ),
                {"my_value": MyModelWithDefault.MyEnum.A},
                (True, False),
            ),
        ],
    )
    async def test_initial_values(self, app, result, enabled):
        """Form object has default model value at startup."""
        async with app.run_test():
            my_form = app.query_one(Form)
            option_1, option_2 = app.query(".option_container").nodes

            _check_state(option_1, enabled[0])
            _check_state(option_2, enabled[1])
            assert my_form.obj == result

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "app,value",
        [
            (MyApp(MyModel), "A"),
            (MyApp(MyModelWithDefault), MyModelWithDefault.MyEnum.A),
        ],
    )
    async def test_manual_input(self, app, value):
        async with app.run_test() as pilot:
            my_form = app.query_one(Form)
            option_1, option_2 = app.query(".option_container").nodes

            await _click_option_container(option_1, pilot)
            _check_state(option_1, True)
            _check_state(option_2, False)
            assert my_form.obj == {"my_value": value}


class TestNestedMultipleWidgets:
    """Multiple widgets representing a single pydantic field.

    Using the textual test frame work we create an app with a form
    containing multiple widgets representing a single pydantic field.
    """

    class MyModel(BaseModel):
        """The model which creates multiple field widgets.
        It will create the following form:
        ____________________________________________________
        |                                                    |
        |  my_value:                                         |
        |      [ ] A                                         |
        |      [ ] manual input _______________              |
        |                                                    |
        |                         [ OK ][ CANCEL ]           |
        |____________________________________________________|

        """

        my_value: Literal["A"] | int

    class MyModelWithDefault(BaseModel):
        """Same as above, but with a default value."""

        my_value: Literal["A"] | int = 5

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "app,result,enabled",
        [
            (MyApp(MyModel), {}, (False, False)),
            (MyApp(MyModelWithDefault), {"my_value": "5"}, (False, True)),
            (
                MyApp(MyModelWithDefault, MyModelWithDefault(my_value="A")),
                {"my_value": "A"},
                (True, False),
            ),
        ],
    )
    async def test_initial_values(self, app, result, enabled):
        """Form object has default model value at startup."""
        async with app.run_test():
            my_form = app.query_one(Form)
            option_1, option_2 = app.query(".option_container").nodes

            _check_state(option_1, enabled[0])
            _check_state(option_2, enabled[1])
            assert my_form.obj == result

    @pytest.mark.asyncio
    async def test_manual_input(self):
        app = MyApp(self.MyModel)
        async with app.run_test() as pilot:
            my_form = app.query_one(Form)
            option_1, int_input = app.query(".option_container").nodes

            # select the first option
            await _click_option_container(option_1, pilot)
            _check_state(option_1, True)
            _check_state(int_input, False)
            assert my_form.obj == {"my_value": "A"}

            # select the second option
            await _click_option_container(int_input, pilot)
            inp = int_input.query_one(Input)
            inp.focus()
            await pilot.press(*list("123"))
            _check_state(option_1, False)
            _check_state(int_input, True)
            assert my_form.obj == {"my_value": "123"}


class TestSubModel:
    class MyModel(BaseModel):
        class SubModel(BaseModel):
            my_value: str = "some_default"

        my_sub_model: SubModel

    class MyModelWithDefault(BaseModel):
        class SubModel(BaseModel):
            my_value: str = "some_default"

        my_sub_model: SubModel = SubModel()

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "app,result",
        [
            (MyApp(MyModel), {}),
            (
                MyApp(MyModelWithDefault),
                {"my_sub_model": MyModelWithDefault.SubModel()},
            ),
            (
                MyApp(
                    MyModelWithDefault,
                    MyModelWithDefault(**{"my_sub_model": {"my_value": "A"}}),
                ),
                {"my_sub_model": MyModelWithDefault.SubModel(**{"my_value": "A"})},
            ),
        ],
    )
    async def test_initial_values(self, app, result):
        """Form object has default model value at startup."""
        async with app.run_test():
            my_form = app.query_one(Form)

            assert my_form.obj == result

    @pytest.mark.asyncio
    async def test_manual_input(self):
        app = MyApp(self.MyModel)

        async with app.run_test() as pilot:
            my_main_model_form = app.query_one(Form)

            # this will push a new form with SubModel as form data.
            await pilot.click("#edit_button")

            # Return to the previous screen (with model MyMainModel) by cancelling.
            await pilot.click("#cancel")
            assert my_main_model_form.obj == {}

            # Open the submodel form again.
            await pilot.click("#edit_button")
            # Return to the previous screen (with model MyMainModel) but now by "OK".
            await pilot.click("#ok")
            assert my_main_model_form.obj == {
                "my_sub_model": self.MyModel.SubModel(**{"my_value": "some_default"})
            }

            # open the form again to edit the SubModel
            await pilot.click("#edit_button")

            # get the input field for the "my_value" property of the SubModel
            sub_model_form = app.query(Form).last()
            inp = sub_model_form.query_one(Input)
            inp.clear()
            inp.focus()

            await pilot.press(*list("Another value"))
            # we make sure the object is updated.
            assert sub_model_form.obj == {"my_value": "Another value"}

            # but we cancel and check whether we have still the previous value.
            await pilot.click("#cancel")
            assert my_main_model_form.obj == {
                "my_sub_model": self.MyModel.SubModel(**{"my_value": "some_default"})
            }


@pytest.mark.asyncio
async def test_option_container_double_click():
    """Multiple clicks on option group does not change state.

    An option container is always part of a group. Inside this group
    only one option can be active and you can not "unselect" an option
    by clicking it a second time.
    """

    class MyModel(BaseModel):
        my_value: Literal["A", "B"]

    app = MyApp(MyModel)

    async with app.run_test() as pilot:
        form = app.query_one(Form)
        option_1, option_2 = app.query(".option_container").nodes

        await _click_option_container(option_1, pilot)
        _check_state(option_1, True)
        _check_state(option_2, False)
        assert form.obj == {"my_value": "A"}

        # doing an identical click. check whether nothing has changed.
        await _click_option_container(option_1, pilot)
        _check_state(option_1, True)
        _check_state(option_2, False)
        assert form.obj == {"my_value": "A"}
