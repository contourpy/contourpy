from __future__ import annotations

import sys
from typing import Any

from docutils.parsers.rst import Directive
from docutils.parsers.rst.directives import unchanged

import contourpy

sys.path.insert(0, '.')
from table import Table


class NameSupports(Directive):
    optional_arguments = 1

    option_spec = {
        "filter": unchanged,
    }

    def run(self) -> list[Any]:
        names = list(contourpy._class_lookup)
        classes = list(contourpy._class_lookup.values())
        function_names = [
            "supports_corner_mask",
            "supports_quad_as_tri",
            "supports_threads",
            "supports_z_interp",
        ]

        filter_string = self.options.get("filter")
        if filter_string is not None:
            function_name = f"supports_{filter_string}"
            if function_name not in function_names:
                raise ValueError(f"Invalid filter string '{filter_string}'")
            function_names = [function_name]

        table = Table(1 + len(names))
        table.add_header([""] + names)

        for function_name in function_names:
            row = [function_name]
            for cls in classes:
                func = getattr(cls, function_name)
                if func():
                    row.append("Yes")
                else:
                    row.append("")
            table.add_row(row)

        return [table.get()]


def setup(app: Any) -> dict[str, bool]:
    app.add_directive("name_supports", NameSupports)
    return {'parallel_read_safe': True, 'parallel_write_safe': True}
