from __future__ import annotations

import dataclasses
from typing import Any, TypedDict


class Font(TypedDict, total=False):
    # plotly/graph_objs/scatter/legendgrouptitle/_font.py
    color: str | None
    family: str | None
    lineposition: str | None
    shadow: str | None
    size: int | float | None
    style: str | None
    textcase: str | None
    variant: str | None
    weight: int | None


class Legendgrouptitle(TypedDict, total=False):
    # plotly/graph_objs/scatter/_legendgrouptitle.py
    text: str | None
    font: Font | None


@dataclasses.dataclass
class LegendContext:
    name: str
    showlegend: bool
    legendgroup: str | int | float | None = None
    legendgrouptitle: Legendgrouptitle | None = None

    @property
    def trace_kwargs(self) -> dict[str, Any]:
        return dataclasses.asdict(self)


class LegendContextManager:
    def __init__(self, legendgroup: bool) -> None:
        super().__init__()
        self.legendgroup = legendgroup
        self._seen_labels: set[str] = set()

    def get_legend_ctx(self, label: str) -> LegendContext:
        if not self.legendgroup:
            return LegendContext(name=label, showlegend=True)
        if label not in self._seen_labels:
            self._seen_labels.add(label)
            return LegendContext(
                name=label,
                showlegend=True,
                legendgroup=label,
                # FIXME: This doesn't seem to work as expected
                # legendgrouptitle=Legendgrouptitle(text=label),
            )
        return LegendContext(
            name=label,
            showlegend=False,
            legendgroup=label,
        )
