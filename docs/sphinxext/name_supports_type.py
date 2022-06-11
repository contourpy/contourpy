import sys

from docutils.parsers.rst import Directive

import contourpy

sys.path.insert(0, '.')
from sphinxext.table import Table


class NameSupportsType(Directive):
    required_arguments = 1

    def run(self):
        if self.arguments[0] not in ("LineType", "FillType"):
            raise ValueError(f"Do not recognise argument {self.arguments[0]}")

        type_name = self.arguments[0]
        lowercase_name = type_name.replace(r"Type", "_type").lower()
        default_func_name = f"default_{lowercase_name}"
        supports_func_name = f"supports_{lowercase_name}"
        type_enum = getattr(contourpy, type_name)

        names = list(contourpy._class_lookup)
        classes = list(contourpy._class_lookup.values())
        default_types = [getattr(cls, default_func_name).name for cls in classes]

        table = Table(1 + len(names))
        table.add_header([type_name] + names)
        for name, enum in dict(type_enum.__members__).items():
            row = [name]
            for cls, default_type in zip(classes, default_types):
                func = getattr(cls, supports_func_name)
                if func(enum):
                    cell = "✔️"
                    if name == default_type:
                        cell += " default"
                    row.append(cell)
                else:
                    row.append("")
            table.add_row(row)

        return [table.get()]


def setup(app):
    app.add_directive("name_supports_type", NameSupportsType)
    return {'parallel_read_safe': True, 'parallel_write_safe': True}
