from __future__ import annotations

import re
from typing import TYPE_CHECKING, Any

from asv.util import human_value
from loader import Loader
import matplotlib.pyplot as plt
import numpy as np

from contourpy import FillType, LineType

if TYPE_CHECKING:
    from matplotlib.axes import Axes
    from matplotlib.patches import Rectangle


# Default fill/line types that exist in all algorithms.
default_fill_type = FillType.OuterCode
default_line_type = LineType.SeparateCode


def capital_letters_to_newlines(text: str) -> str:
    return re.sub(r"([a-z0-9])([A-Z])", r"\1\n\2", text)


def get_corner_mask_label(corner_mask: bool | str) -> str:
    if corner_mask == "no mask":
        return "no mask"
    else:
        return f"corner_mask={corner_mask}"


def get_style(name: str, corner_mask: bool | str) -> tuple[str, str, str, float]:
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

    edge_color = "#222222"

    return colors[name], edge_color, hatches[corner_mask], 0.5


def with_time_units(value: float, error: float | None = None) -> str:
    # ASV's human_value() doesn't put a space between numbers and units.
    # See e.g. https://physics.nist.gov/cuu/Units/checklist.html
    with_units = human_value(value, "seconds", error)
    return re.sub(r"(?<=\S)([a-zA-Z]+)$", r" \1", with_units)


def by_name_and_type(loader: Loader, filled: bool, dataset: str, render: bool, n: int) -> None:
    show_error = False
    corner_masks: list[str | bool] = ["no mask", False, True]
    filled_str = "filled" if filled else "lines"
    title = f"{filled_str} {dataset} n={n} {'(calculate and render)' if render else ''}"

    nbars = 3
    width = 1.0 / (nbars + 1)
    ntypes = len(FillType.__members__) if filled else len(LineType.__members__)
    cache = {}  # Results cache

    for mode in ["light", "dark"]:
        plt.style.use("default" if mode == "light" else "dark_background")

        fig, ax = plt.subplots(figsize=(8.5, 6))
        xticklabels = []

        for name in ["mpl2005", "mpl2014", "serial"]:
            bname = "serial" if name == "serial" else "mpl20xx"
            benchmarks_name = f"time_{filled_str}_{bname}{'_render' if render else ''}"

            if name == "serial":
                xs = 2 + np.arange(ntypes)
            else:
                xs = np.array(0 if name == "mpl2005" else 1)  # type: ignore[assignment]

            i = 0
            for corner_mask in corner_masks:
                kwargs = {"name": name, "dataset": dataset, "corner_mask": corner_mask, "n": n}

                results = loader.get(benchmarks_name, **kwargs)
                if results["name"] != name:
                    raise RuntimeError(f"Loader returning wrong name: {name} != {results['name']}")

                if results["mean"] is None:
                    continue

                name = results["name"]
                mean = results["mean"]
                error = results["error"]
                types = results["fill_type" if filled else "line_type"]
                if not isinstance(types, list):
                    types = [types]

                if mode == "light":
                    for m, t in zip(mean, types):
                        cache[(name, t, corner_mask)] = m

                color, edge_color, hatch, line_width = get_style(name, corner_mask)
                offset = width*(i - 0.5*(nbars - 1))
                label = f"{name} {get_corner_mask_label(corner_mask)}"
                yerr = error if show_error else None
                mean = np.asarray(mean, dtype=np.float64)  # None -> nan.
                if corner_mask == "no mask":
                    xticklabels += [name + str(t).split(".")[1] for t in types]

                rects = ax.bar(
                    xs + offset, mean, width, yerr=yerr, color=color, edgecolor=edge_color,
                    hatch=hatch, linewidth=line_width, capsize=4, label=label, zorder=3)
                if show_error:
                    labels = [with_time_units(m, s) for m, s in zip(mean, error)]
                else:
                    labels = [with_time_units(m) for m in mean]
                ax.bar_label(rects, labels, padding=5, rotation="vertical", size="medium")

                i += 1

        if filled and not render:
            if dataset == "random":
                ax.set_ylim(0, 3.3)
            else:
                ax.set_ylim(0, 0.27)
        elif filled and render and dataset == "simple":
            ax.set_ylim(0, 0.41)
        elif not filled and render and dataset == "simple":
            ax.set_ylim(0, 0.38)
        else:
            ax.set_ylim(0, ax.get_ylim()[1]*1.1)  # Magic number.

        loc: str | tuple[float, float] = "best"
        if not filled and render and dataset == "random":
            loc = "lower left"
        elif render and dataset == "simple":
            loc = "lower right"
        elif filled and render and dataset == "random":
            loc = (0.51, 0.6)
        ax.legend(loc=loc, framealpha=0.9)

        ax.grid(axis="y", c="k" if mode == "light" else "w", alpha=0.2)
        ax.set_xticks(np.arange(ntypes+2))
        xticklabels = list(map(capital_letters_to_newlines, xticklabels))
        ax.set_xticklabels(xticklabels)
        ax.set_ylabel("Time (seconds)")
        ax.set_title(title)
        for spine in ax.spines.values():
            spine.set_zorder(5)
        fig.tight_layout()

        filename = f"{filled_str}_{dataset}_{n}{'_render' if render else ''}_{mode}.svg"
        #print(f"Saving {filename}")
        fig.savefig(filename, transparent=True)

    # Print comparison of different algorithms using mpl default type.
    print(f"Times and speedups: {filled_str} dataset={dataset} render={render}")
    default_type = FillType.OuterCode if filled else LineType.SeparateCode
    for target in ["mpl2005", "mpl2014"]:
        names = ["serial", target]
        for m in ("no mask", False, True):
            if names[1] == "mpl2005" and m is True:
                continue
            times = [cache[(name, default_type, m)] for name in names]
            ratio = times[0]/times[1]
            print(f"  {ratio:.3f}, {1.0/ratio:.3f}, {names[0]}:{names[1]}, {default_type}, {m}")
        print()

    # Print comparison of different line/fill types for serial algorithm.
    name = "serial"
    for t in (FillType.__members__.values() if filled else LineType.__members__.values()):
        if t == default_type:
            continue
        for m in ("no mask", False, True):
            times = [cache[(name, t, m)], cache[(name, default_type, m)]]
            ratio = times[0]/times[1]
            print(f"  {ratio:.3f}, {1.0/ratio:.3f}, {name}, {t}:{default_type}, {m}")
    print()


def comparison_two_benchmarks(
    loader: Loader, filled: bool, dataset: str, varying: str, varying_values: list[float],
) -> None:
    if varying == "thread_count":
        file_prefix = "threaded"
    elif varying == "total_chunk_count":
        file_prefix = "chunk"
    else:
        raise RuntimeError(f"Invalid varying field '{varying}'")

    show_error = False
    show_speedups = (varying == "thread_count")
    n = 1000
    corner_mask = "no mask"

    filled_str = "filled" if filled else "lines"
    kwargs: dict[str, Any] = {"dataset":dataset, "corner_mask": corner_mask, "n": n}
    if varying == "thread_count":
        kwargs["total_chunk_count"] = 40

    name0 = "serial"
    name1 = "threaded" if varying == "thread_count" else "serial"

    kwargs["name"] = name0
    if varying == "thread_count":
        benchmarks_name = f"time_{filled_str}_{name0}_chunk"
    else:
        benchmarks_name = f"time_{filled_str}_{name0}"
    results = loader.get(benchmarks_name, **kwargs)
    fill_or_line_type = results["fill_type"] if filled else results["line_type"]
    ntype = len(fill_or_line_type)
    mean0 = results["mean"]
    error0 = results["error"]

    kwargs["name"] = name1
    kwargs[varying] = varying_values
    if varying == "thread_count":
        benchmarks_name = f"time_{filled_str}_{name1}"
    else:
        benchmarks_name = f"time_{filled_str}_{name1}_chunk"
    results = loader.get(benchmarks_name, **kwargs)
    mean1 = results["mean"]
    error1 = results["error"]

    varying_count = len(varying_values)
    xs = np.arange(ntype*(varying_count+2))
    xs.reshape((ntype, varying_count+2))

    speedups = np.expand_dims(mean0, axis=1) / np.reshape(mean1, (ntype, varying_count))
    speedups_flat = speedups.ravel()

    def in_bar_label(ax: Axes, rect: Rectangle, value: str) -> None:
        kwargs: dict[str, Any] = {"fontsize": "medium", "ha": "center", "va": "bottom",
                                  "color": "k"}
        if varying != "thread_count":
            kwargs["rotation"] = "vertical"
        ax.annotate(value, (rect.xy[0] + 0.5*rect.get_width(), rect.xy[1]), **kwargs)

    for mode in ["light", "dark"]:
        plt.style.use("default" if mode == "light" else "dark_background")
        fig, ax = plt.subplots(figsize=(8.5, 6))

        # Serial bars.
        color, edge_color, hatch, line_width = get_style(name0, corner_mask)
        if varying == "thread_count":
            label = f"{name0} {get_corner_mask_label(corner_mask)}"
        else:
            label = None
        rects = ax.bar(xs[:, 0], mean0, width=1, color=color, edgecolor=edge_color, hatch=hatch,
                       linewidth=line_width, label=label, zorder=3)
        if show_error:
            labels = [with_time_units(m, s) for m, s in zip(mean0, error0)]
        else:
            labels = [with_time_units(m) for m in mean0]
        ax.bar_label(rects, labels, padding=5, rotation="vertical", size="medium")
        if varying != "thread_count":
            for rect in rects:
                in_bar_label(ax, rect, " 1")

        # Threaded bars.
        color, edge_color, hatch, line_width = get_style(name1, corner_mask)
        label = varying.replace("_", " ")
        label = f"{name1} {get_corner_mask_label(corner_mask)}\n({label} shown at bottom of bar)"
        rects = ax.bar(xs[:, 1:-1].ravel(), mean1, width=1, color=color, edgecolor=edge_color,
                       hatch=hatch, linewidth=line_width, label=label, zorder=3)
        labels = []
        for i, (mean, error, speedup) in enumerate(zip(mean1, error1, speedups_flat)):
            if show_error:
                label = with_time_units(mean, error)
            else:
                label = with_time_units(mean)
            if show_speedups and i % varying_count > 0:
                label += f" (x {speedup:.2f})"
            labels.append(label)
        ax.bar_label(rects, labels, padding=5, rotation="vertical", size="medium")
        for rect, value in zip(rects, np.tile(varying_values, ntype)):
            in_bar_label(ax, rect, f" {value}")

        if dataset == "random":
            ymax = 1.9 if filled else 1.4
        elif varying == "thread_count":
            ymax = ax.get_ylim()[1]*1.32
        else:
            ymax = ax.get_ylim()[1]*1.25
        ax.set_ylim(0, ymax)

        ax.set_xticks(xs[:, 0] + 0.5*varying_count)
        xticklabels = [str(t).split(".")[1] for t in fill_or_line_type]
        xticklabels = list(map(capital_letters_to_newlines, xticklabels))
        ax.set_xticklabels(xticklabels)

        ax.legend(loc="upper right", framealpha=0.9)
        ax.grid(axis="y", c="k" if mode == "light" else "w", alpha=0.2)
        ax.set_ylabel("Time (seconds)")
        ax.set_title(f"{filled_str} {dataset} n={n}")
        fig.tight_layout()

        filename = f"{file_prefix}_{filled_str}_{dataset}_{mode}.svg"
        #print(f"Saving {filename}")
        fig.savefig(filename, transparent=True)

    if varying == "total_chunk_count":
        # Print comparison of different algorithms using mpl default type.
        print(f"Times and speedups: varying={varying} {filled_str} dataset={dataset}")
        for i, t in enumerate(fill_or_line_type):
            min_, max_ = speedups[i].min(), speedups[i].max()
            print(f"  {1.0/max_:.3f}-{1.0/min_:.3f}, {min_:.3f}-{max_:.3f}, {t}")
        print()


def main() -> None:
    loader = Loader()

    print(f"Saving benchmark plots for machine={loader.machine} commit={loader.commit[:7]}")

    for render in [False, True]:
        for filled in [False, True]:
            for dataset in ["simple", "random"]:
                by_name_and_type(loader, filled, dataset, render, 1000)

    for filled in [False, True]:
        for dataset in ["simple", "random"]:
            comparison_two_benchmarks(loader, filled, dataset, "total_chunk_count",
                                      [4, 12, 40, 120])

    for filled in [False, True]:
        for dataset in ["simple", "random"]:
            comparison_two_benchmarks(loader, filled, dataset, "thread_count", [1, 2, 4, 6])


if __name__ == "__main__":
    main()
