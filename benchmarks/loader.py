from __future__ import annotations

from copy import deepcopy
from datetime import datetime
from typing import Any

from asv.benchmark import Benchmark
from asv.benchmarks import Benchmarks
from asv.config import Config
from asv.results import Results, iter_results_for_machine
from asv.statistics import get_err

from contourpy import FillType, LineType


class Loader:
    _config: Config
    _benchmarks: Benchmarks
    _machine: str
    _results: Results

    def __init__(self, machine: str | None = None) -> None:
        self._config = Config.load()
        self._benchmarks = Benchmarks.load(self._config)

        if machine is None:
            import platform
            machine = platform.uname()[1]

        latest_results = None
        for results in iter_results_for_machine(self._config.results_dir, machine):
            if latest_results is None or results.date > latest_results.date:
                latest_results = results
        if latest_results is None:
            raise RuntimeError("No results found for machine {machine}")
        print(latest_results.commit_hash, datetime.fromtimestamp(latest_results.date/1000.0))

        self._results = latest_results
        self._machine = machine

    def _find_benchmark_by_name(self, name: str) -> Benchmark:
        for k, v in self._benchmarks.items():
            if k.endswith(name):
                return v
        raise RuntimeError(f"Cannot find benchmark with name {name}")

    @property
    def commit(self) -> str:
        return self._results.commit_hash  # type: ignore[no-any-return]

    def get(self, benchmark_name: str, **kwargs: Any) -> dict[str, Any]:
        benchmark = self._find_benchmark_by_name(benchmark_name)
        param_names = benchmark["param_names"]
        params = deepcopy(benchmark["params"])
        for name, value in kwargs.items():
            index = param_names.index(name)
            if isinstance(value, list):
                params[index] = [repr(item) for item in value]
            else:
                params[index] = [repr(value)]

        stats = self._results.get_result_stats(benchmark["name"], params)
        values = self._results.get_result_value(benchmark["name"], params)

        ret = {}
        for name, param in zip(param_names, params):
            for i, item in enumerate(param):
                if isinstance(item, str):
                    if item[0] == "'" and item[-1] == "'":
                        item = item[1:-1]

                    if item.startswith("<FillType"):
                        item = FillType(int(item[item.index(" "):-1]))
                    elif item.startswith("<LineType"):
                        item = LineType(int(item[item.index(" "):-1]))
                    elif item == "False":
                        item = False
                    elif item == "True":
                        item = True
                    else:
                        try:
                            item = int(item)
                        except ValueError:
                            pass
                    param[i] = item
            ret[name] = param[0] if len(param) == 1 else param

        if values[0] is None:
            ret["mean"] = ret["error"] = None
        else:
            ret["mean"] = values
            ret["error"] = [get_err(v, s) for v, s in zip(values, stats)]

        return ret

    @property
    def machine(self) -> str:
        return self._machine
