import sys

from docutils.parsers.rst import Directive
from docutils.parsers.rst.directives import unchanged

import contourpy

sys.path.insert(0, '.')
from sphinxext.table import Table


class NameSupports(Directive):
    optional_arguments = 1

    option_spec = {
        "filter": unchanged,
    }

    def run(self):
        names = list(contourpy._class_lookup)
        classes = list(contourpy._class_lookup.values())
        function_names = [
            "supports_corner_mask",
            "supports_quad_as_tri",
            "supports_threads",
            "supports_z_interp",
        ]

        filter_ = self.options.get("filter")
        if filter_ is not None:
            function_names = filter(lambda str: filter_ in str, function_names)

        table = Table(1 + len(names))
        table.add_header([""] + names)

        for function_name in function_names:
            row = [function_name]
            for cls in classes:
                func = getattr(cls, function_name)
                if func():
                    row.append("✔️")
                else:
                    row.append("")
            table.add_row(row)

        return [table.get()]


def setup(app):
    app.add_directive("name_supports", NameSupports)
    return {'parallel_read_safe': True, 'parallel_write_safe': True}
