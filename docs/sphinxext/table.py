from __future__ import annotations

from collections.abc import Sequence
from typing import Any

from docutils import nodes


class Table:
    _ncols: int
    _table: Any
    _tbody: Any
    _tgroup: Any

    def __init__(self, ncols: int) -> None:
        self._ncols = ncols
        self._table = nodes.table()
        self._tgroup = nodes.tgroup(cols=ncols)
        for _ in range(ncols):
            colspec = nodes.colspec(colwidth=1)
            self._tgroup.append(colspec)
        self._table += self._tgroup
        self._tbody = None

    def add_header(self, items: Sequence[Any]) -> None:
        if len(items) != self._ncols:
            raise RuntimeError(f"Expect {self._ncols} header items but {len(items)} specified")

        thead = nodes.thead()
        self._tgroup += thead

        row = nodes.row()
        thead += row

        for item in items:
            entry = nodes.entry()
            row += entry
            entry += nodes.paragraph(text=item)

    def add_row(self, items: Sequence[Any]) -> None:
        if len(items) != self._ncols:
            raise RuntimeError(f"Expect {self._ncols} row items but {len(items)} specified")

        if self._tbody is None:
            self._tbody = nodes.tbody()
            self._tgroup += self._tbody

        row = nodes.row()
        self._tbody += row

        for item in items:
            entry = nodes.entry()
            row += entry
            entry += nodes.paragraph(text=item)

    def get(self) -> Any:
        return self._table
