import os

from docutils import nodes
from docutils.parsers.rst.directives import choice
from sphinx.directives.code import CodeBlock

from contourpy.util.mpl_renderer import MplRenderer


class PlotDirective(CodeBlock):
    has_content = True
    optional_arguments = 1

    option_spec = {
        "source-position": lambda x: choice(x, ("below", "above", "none")),
    }

    latest_image_index = {}  # dict of string docname -> latest image index used.

    def _temporary_show(self, renderer, image_filenames):
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

    def run(self):
        source_position = self.options.get("source-position", "below")

        source = self.content
        combined_source = "\n".join(source)

        svg_filenames = []

        # Temporarily replace MplRenderer.show() to save to SVG file and include SVG files in
        # sphinx output. Should probably be in a context manager instead.
        old_show = getattr(MplRenderer, "show")
        setattr(MplRenderer, "show", lambda renderer: self._temporary_show(renderer, svg_filenames))
        exec(combined_source)
        setattr(MplRenderer, "show", old_show)

        images = []
        for svg_filename in svg_filenames:
            image = nodes.image(uri=svg_filename)
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


def setup(app):
    app.add_directive("plot", PlotDirective)
    return {'parallel_read_safe': True, 'parallel_write_safe': True}
