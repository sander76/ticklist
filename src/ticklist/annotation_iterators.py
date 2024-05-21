"""Annotation iterators."""

from __future__ import annotations

from enum import Enum
from inspect import isclass
from types import UnionType
from typing import Any, Collection, Iterable, Literal, get_args

from pydantic import BaseModel

from ticklist.field_data import (
    FieldData,
    FieldDataForEnumValue,
    FieldDataForInt,
    FieldDataForLiteralValue,
    FieldDataForModel,
    FieldDataForString,
)
from ticklist.types import AnnotationIterator


class StringAndLiteralAnnotationNotAllowed(Exception):
    """A combination of `Literal` and `str` is not allowed.

    It can produce unwanted results.
    Consider this example:

    ```python
    class MyModel(BaseModel):
        my_value: Literal['B','A'] | str = 'A'
    ```

    All annotations are traversed (Literal['A'], Literal['B'] and str) and
    evaluated with the default value of 'A'. This will match on both the
    Literal['A'] and the str, activating both, which is an error.

    An alternative to the Literal would be the use of an Enum.
    """

    def __init__(self, annotation: Any) -> None:
        """Init.

        Args:
            annotation: The failing annotation.
        """
        self.annotation = annotation
        super().__init__(
            f"Annotation with `Literal` AND `str` is not allowed. {self.annotation=}"
        )


def field_data_from_annotation(
    annotation: Any,
    key: str,
    value: Any,
    default: Any,
    annotation_iterators: Collection[AnnotationIterator],
) -> tuple[FieldData, ...]:
    """Extract FieldData objects from annotation information.

    Args:
        annotation: The type annotation.
        key: The key of the (pydantic) field.
        value: An optional value of the key.
        default: An optional default value of the key.
        annotation_iterators: A collection of annotation iterators.

    Raises:
        StringAndLiteralAnnotationNotAllowed: _description_

    Returns:
        _description_
    """
    field_data = tuple(
        _iter_over_annotation(annotation, key, value, default, annotation_iterators)
    )

    _field_data_types = set((fd.__class__ for fd in field_data))

    if ({FieldDataForString, FieldDataForLiteralValue}).issubset(_field_data_types):
        raise StringAndLiteralAnnotationNotAllowed(annotation)

    return field_data


def bool_type_iterator(
    annotation: Any, key: str, value: Any, default: Any
) -> Iterable[Any]:
    """Yield values for a boolean annotation."""
    if annotation is bool:
        yield "True"
        yield "False"


def enum_type_iterator(
    annotation: Any, key: str, value: Any, default: Any
) -> Iterable[Any]:
    """Yield values for an enum annotation."""
    if isclass(annotation) and issubclass(annotation, Enum):
        for anno in annotation:
            yield anno


def enum_item_type_iterator(
    annotation: Any, key: str, value: Any, default: Any
) -> Iterable[FieldDataForEnumValue]:
    """Yield value for an individual enum item."""
    if isinstance(annotation, Enum):
        yield FieldDataForEnumValue.parse(annotation, key, value, default)


def str_type_iterator(
    annotation: Any, key: str, value: Any, default: Any
) -> Iterable[FieldDataForString]:
    """Yield value for a string annotation."""
    if isclass(annotation) and issubclass(annotation, str):
        yield FieldDataForString.parse(annotation, key, value, default)


def int_type_iterator(
    annotation: Any, key: str, value: Any, default: Any
) -> Iterable[FieldDataForInt]:
    """Yield value of an int annotation."""
    if isclass(annotation) and issubclass(annotation, int):
        yield FieldDataForInt.parse(annotation, key, value, default)


def union_type_iterator(
    annotation: Any, key: str, value: Any, default: Any
) -> Iterable[Any]:
    """Yield values for a union annotation."""
    # Nowadays Unions are created using the pipe | character, where earlier
    # a typing.Union was used. Both are also stored differently
    # (Inside the __annotation__ property
    # or the FieldInfo.annotation of a pydantic field).
    #
    # A bit more strange is that in some situations even when using the pipe | character
    # the annotation is still stored in the old style.
    # This at least appears when a Literal type is involved. This might change
    # in future python version, but for now, this union check looks for both
    # union styles.
    if isinstance(annotation, UnionType):
        yield from get_args(annotation)
    elif getattr(annotation, "__name__", None) in ("Optional", "Union"):
        yield from get_args(annotation)


def model_type_iterator(
    annotation: Any, key: str, value: Any, default: Any
) -> Iterable[Any]:
    """Yield value for a pydantic BaseModel annotation."""
    if isclass(annotation) and issubclass(annotation, BaseModel):
        yield FieldDataForModel.parse(annotation, key, value, default)


def literal_type_iterator(
    annotation: Any, key: str, value: Any, default: Any
) -> Iterable[Any]:
    """Yield values for a Literal annotation."""
    origin = getattr(annotation, "__origin__", None)
    if origin is Literal:
        yield from get_args(annotation)


def literal_value_iterator(
    annotation: Any, key: str, value: Any, default: Any
) -> Iterable[FieldDataForLiteralValue]:
    """Yield values for a Literal Value annotation."""
    if isinstance(annotation, str):
        yield FieldDataForLiteralValue.parse(annotation, key, value, default)


ANNOTATION_ITERATORS: tuple[AnnotationIterator, ...] = (
    bool_type_iterator,
    enum_type_iterator,
    enum_item_type_iterator,
    str_type_iterator,
    int_type_iterator,
    union_type_iterator,
    model_type_iterator,
    literal_type_iterator,
    literal_value_iterator,
)


def _iter_over_annotation(
    annotation: Any,
    key: str,
    value: Any,
    default: Any,
    annotation_iterators: Collection[AnnotationIterator],
) -> Iterable[FieldData]:
    if isinstance(annotation, FieldData):
        yield annotation

    else:
        found = False
        for annotation_iterator in annotation_iterators:
            for _annotation in annotation_iterator(annotation, key, value, default):
                found = True
                yield from _iter_over_annotation(
                    _annotation, key, value, default, annotation_iterators
                )
            if found:
                break
        else:
            raise ValueError(f"No FieldDataType found for {annotation}")
