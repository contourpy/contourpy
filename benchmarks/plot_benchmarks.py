from asv.util import human_value
from contourpy import FillType, LineType
from loader import Loader
import matplotlib.pyplot as plt
import numpy as np
import re


# Default fill/line types that exist in all algorithms.
default_fill_type = FillType.OuterCode
default_line_type = LineType.SeparateCode


def capital_letters_to_newlines(text):
    return re.sub(r"([a-z0-9])([A-Z])", r"\1\n\2", text)


def get_corner_mask_label(corner_mask):
    if corner_mask == "no mask":
        return "no mask"
    else:
        return f"corner_mask={corner_mask}"


def get_style(name, corner_mask):
    # Colors from Paul Tol's colorblind friendly light scheme (https://personal.sron.nl/~pault)
    colors = {
        "mpl2005": "#eedd88",   # light yellow.
        "mpl2014": "#ee8866",   # orange.
        "serial": "#77aadd",    # light blue.
        "threaded": "#99ddff",  # light cyan.
    }

    hatches = {
        "no mask": "",
        False: "---",
        True: "///",
    }

    return colors[name], "#444444", hatches[corner_mask], 0.5


def by_name_and_type(loader, filled, dataset, render, n):
    show_error = False
    corner_masks = ["no mask", False, True]
    filled_str = "filled" if filled else "lines"
    title = f"{filled_str} {dataset} n={n} {'(calculate and render)' if render else ''}"

    fig, ax = plt.subplots(figsize=(8.5, 6))
    nbars = 3
    width = 1.0 / (nbars + 1)
    ntypes = len(FillType.__members__ if filled else LineType.__members__)
    xticklabels = []

    for name in ["mpl2005", "mpl2014", "serial"]:
        bname = "serial" if name == "serial" else "mpl20xx"
        benchmarks_name = f"time_{filled_str}_{bname}{'_render' if render else ''}"

        if name == "serial":
            xs = 2 + np.arange(ntypes)
        else:
            xs = np.array((0 if name == "mpl2005" else 1))

        i = 0
        for corner_mask in corner_masks:
            kwargs = dict(name=name, dataset=dataset, corner_mask=corner_mask, n=n)

            results = loader.get(benchmarks_name, **kwargs)
            if results["name"] != name:
                raise RuntimeError("Loader returning wrong name: {name} != {results['name']}")

            if results["mean"] is None:
                continue

            name = results["name"]
            mean = results["mean"]
            std = results["std"]
            if corner_mask == "no mask":
                types = results["fill_type" if filled else "line_type"]
                if not isinstance(types, list):
                    types = [types]
                xticklabels += [name + str(t).split(".")[1] for t in types]

            color, edge_color, hatch, line_width = get_style(name, corner_mask)
            offset = width*(i - 0.5*(nbars - 1))
            label = f"{name} {get_corner_mask_label(corner_mask)}"
            yerr = std if show_error else None
            mean = np.asarray(mean, dtype=np.float64)  # None -> nan.

            rects = ax.bar(
                xs + offset, mean, width, yerr=yerr, color=color, edgecolor=edge_color, hatch=hatch,
                linewidth=line_width, capsize=4, label=label, zorder=3)
            if show_error:
                labels = [human_value(m, "seconds", s) for m, s in zip(mean, std)]
            else:
                labels = [human_value(m, "seconds") for m in mean]
            ax.bar_label(rects, labels, padding=5, rotation="vertical", size="medium")

            i += 1

    if filled and not render and dataset == "random":
        ax.set_ylim(0, 2.7)
    else:
        ax.set_ylim(0, ax.get_ylim()[1]*1.1)  # Magic number.

    loc = "best"
    if not filled and render and dataset == "random":
        loc = "lower left"
    elif render and dataset == "simple":
        loc = "lower right"
    elif filled and render and dataset == "random":
        loc = (0.52, 0.6)
    ax.legend(loc=loc, framealpha=0.9)

    ax.grid(axis='y', c='k', alpha=0.1)
    ax.set_xticks(np.arange(ntypes+2))
    xticklabels = map(capital_letters_to_newlines, xticklabels)
    ax.set_xticklabels(xticklabels)
    ax.set_ylabel("Time (seconds)")
    ax.set_title(title)
    for spine in ax.spines.values():
        spine.set_zorder(5)
    fig.tight_layout()

    filename = f"{filled_str}_{dataset}_{n}{'_render' if render else ''}.png"
    print(f"Saving {filename}")
    fig.savefig(filename, transparent=True)


def by_thread_count(loader, dataset):
    n = 1000
    name = "threaded"
    corner_mask = "no mask"

    def get_label(i):
        label = human_value(mean[i], "seconds")
        if i > 0:
            label += f"\n(x {speedups[i]:.2f})"
        return label

    fig, axes = plt.subplots(ncols=2, figsize=(8, 4))

    for i, filled in enumerate([False, True]):
        filled_str = "filled" if filled else "lines"
        benchmarks_name = f"time_{filled_str}_{name}"
        kwargs = dict(name="threaded", dataset=dataset, corner_mask=corner_mask, n=n)
        results = loader.get(benchmarks_name, **kwargs)

        title = f"{filled_str} {dataset} n={n}"

        thread_count = np.asarray(results["thread_count"])
        mean = np.asarray(results["mean"])
        speedups = mean[0] / mean

        color, edge_color, hatch, line_width = get_style(name, corner_mask)

        ax = axes[i]
        label = f"{name} {get_corner_mask_label(corner_mask)}"
        rects = ax.bar(thread_count, mean, color=color, edgecolor=edge_color, hatch=hatch,
                       linewidth=line_width, label=label, zorder=3)
        labels = [get_label(i) for i in range(len(thread_count))]
        ax.bar_label(rects, labels, padding=5, rotation="vertical", size="medium")

        ax.set_ylim(0, ax.get_ylim()[1]*1.18)  # Magic number.
        ax.grid(axis='y', c='k', alpha=0.1)
        ax.set_xlabel("Thread count")
        ax.set_ylabel("Time (seconds)")
        ax.legend(framealpha=0.9)
        ax.set_title(title)

    fig.tight_layout()

    filename = f"threaded_{dataset}_{n}.png"
    print(f"Saving {filename}")
    fig.savefig(filename, transparent=True)


def main():
    loader = Loader()

    print(f"Saving benchmark plots for machine={loader.machine} commit={loader.commit[:7]}")

    n = 1000
    for filled in [False, True]:
        for dataset in ["random", "simple"]:
            for render in [False, True]:
                #if render and dataset == "simple":
                #    continue
                by_name_and_type(loader, filled, dataset, render, n)

    for dataset in ["random", "simple"]:
        by_thread_count(loader, dataset)


if __name__ == "__main__":
    main()
