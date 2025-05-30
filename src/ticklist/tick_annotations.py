"""Annotations.

Use these inside the `Annotated` part of your pydantic field to modify
the associated widget.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Collection, NotRequired, TypedDict


@dataclass(frozen=True)
class Label:
    """Label annotation.

    Add a custom label to the associated widget.
    """

    value: str


@dataclass(frozen=True)
class BooleanLabels:
    """Boolean labels."""

    label_for_true: str
    label_for_false: str


@dataclass(frozen=True)
class Multiline:
    """A marker class for multiline string fields.

    Args:
        height: The height of the text area in rows. Defaults to 3.
    """

    height: int = 3


class TickAnnotations(TypedDict):
    """All ticked annotations."""

    label: NotRequired[Label]
    boolean_labels: NotRequired[BooleanLabels]
    multiline: NotRequired[Multiline]


def to_tick_annotations(annotations: Collection[Any]) -> TickAnnotations:
    """Filter out all tick annotations."""
    tick_annotations: TickAnnotations = {}
    for anno in annotations:
        match anno:
            case Label():
                tick_annotations["label"] = anno
            case BooleanLabels():
                tick_annotations["boolean_labels"] = anno
            case Multiline():
                tick_annotations["multiline"] = anno
    return tick_annotations
