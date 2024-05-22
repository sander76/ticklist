"""Annotations.

To be used inside the `Annotations` type annotation.
"""

from dataclasses import dataclass
from functools import cache
from inspect import isclass
from typing import Any, Collection, Iterator, NotRequired, TypedDict, TypeVar


@dataclass(frozen=True)
class Label:
    """Label annotation.

    to be used inside an `Annotation` type to indicate the label to be used
    inside the widget.
    """

    value: str


@dataclass(frozen=True)
class BooleanLabels:
    """Boolean labels."""

    label_for_true: str
    label_for_false: str


class TickAnnotations(TypedDict):
    """All ticked annotations."""

    label: NotRequired[Label]
    boolean_labels: NotRequired[BooleanLabels]


def to_tick_annotations(annotations: Collection[Any]) -> TickAnnotations:
    """Filter out all tick annotations."""
    tick_annotations: TickAnnotations = {}
    for anno in annotations:
        match anno:
            case Label():
                tick_annotations["label"] = anno
            case BooleanLabels():
                tick_annotations["boolean_labels"] = anno
    return tick_annotations
