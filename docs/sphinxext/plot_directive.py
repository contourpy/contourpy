from __future__ import annotations

import os
from typing import Any, ClassVar

from docutils import nodes
from docutils.parsers.rst.directives import choice, flag
from sphinx.directives.code import CodeBlock

from contourpy.util.mpl_renderer import MplRenderer


class PlotDirective(CodeBlock):
    has_content = True
    optional_arguments = 2

    option_spec: ClassVar[dict[str, Any]] = {  # type: ignore[misc]
        "separate-modes": flag,
        "source-position": lambda x: choice(x, ("below", "above", "none")),
    }

    # dict of string docname -> latest image index used.
    latest_image_index: ClassVar[dict[str, int]] = {}

    def _mpl_mode_header(self, mode: str) -> str:
        if mode == "light":
            return "import matplotlib.pyplot as plt;plt.style.use('default');\n"
        elif mode == "dark":
            return "import matplotlib as mpl;cycler=mpl.rcParams['axes.prop_cycle'];\n" \
                "import matplotlib.pyplot as plt;plt.style.use('dark_background');\n" \
                "mpl.rcParams['axes.prop_cycle']=cycler;\n"
        else:
            raise ValueError(f"Unexpected mode {mode}")

    def _temporary_show(self, renderer: MplRenderer, image_filenames: list[str]) -> None:
        # Temporary replacement for MplRenderer.show() to save to SVG file instead.
        docname = self.env.docname
        index = self.latest_image_index.get(docname, -1) + 1
        self.latest_image_index[docname] = index

        directory, filename = os.path.split(docname)
        output_directory = os.path.join(directory, "generated")
        if not os.path.isdir(output_directory):
            os.makedirs(output_directory)

        output_filename = f"{filename}_{index}.svg"

        renderer.save(os.path.join(output_directory, output_filename), transparent=True)
        image_filenames.append(os.path.join("generated", output_filename))

    def run(self: Any) -> list[Any]:
        source_position = self.options.get("source-position", "below")

        source = self.content
        combined_source = "\n".join(source)

        using_modes = "separate-modes" in self.options
        modes = ["light", "dark"] if using_modes else ["light"]

        svg_filenames: list[str] = []

        # Temporarily replace MplRenderer.show() to save to SVG file and include SVG files in
        # sphinx output. Should probably be in a context manager instead.
        old_show = getattr(MplRenderer, "show")
        setattr(MplRenderer, "show", lambda renderer: self._temporary_show(renderer, svg_filenames))
        for mode in modes:
            exec(self._mpl_mode_header(mode) + combined_source)
        setattr(MplRenderer, "show", old_show)

        images: list[nodes.Node] = []
        for i, svg_filename in enumerate(svg_filenames):
            image = nodes.image(uri=svg_filename)
            if using_modes:
                mode = modes[i % len(modes)]
                image["classes"].append(f"only-{mode}")
            container = nodes.container()
            container += image
            images += container

        if source_position == "none":
            return images
        else:
            code_block = super().run()
            if source_position == "above":
                return code_block + images
            else:
                return images + code_block


def setup(app: Any) -> dict[str, bool]:
    app.add_directive("plot", PlotDirective)
    return {"parallel_read_safe": True, "parallel_write_safe": True}
