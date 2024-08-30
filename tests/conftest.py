from __future__ import annotations

import glob
import os
import shutil
from typing import TYPE_CHECKING, Any

import pytest

from contourpy import FillType, LineType, ZInterp

if TYPE_CHECKING:
    from collections.abc import Sequence

    from _pytest.fixtures import SubRequest


image_diffs_log: list[str] = []


def pytest_sessionfinish(session: pytest.Session, exitstatus: int) -> None:
    if not session.config.getoption("--log-image-diffs"):
        return

    result_directory = "result_images"
    if not os.path.exists(result_directory):
        os.makedirs(result_directory)

    # Support running in series and parallel via pytest-xdist.
    worker = os.environ.get("PYTEST_XDIST_WORKER", "")
    if worker:
        log_filename = f"image_diffs_{worker}.log"
    else:
        log_filename = "image_diffs.log"
        print(f"\nWriting to {log_filename}")
    log_filename = os.path.join(result_directory, log_filename)

    with open(log_filename, "w") as f:
        for line in image_diffs_log:
            f.write(f"{line}\n")

    if not worker:
        worker_files = glob.glob(os.path.join(result_directory, "image_diffs_*.log"))
        if worker_files:
            # If running in parallel, combine output log files.
            with open(log_filename, "w") as f:
                for worker_file in worker_files:
                    with open(worker_file) as src:
                        shutil.copyfileobj(src, f)
                    os.remove(worker_file)


def pytest_addoption(parser: pytest.Parser) -> None:
    parser.addoption(
        "--runslow", action="store_true", default=False, help="run slow tests",
    )
    parser.addoption(
        "--runtext", action="store_true", default=False, help="run tests with text output",
    )
    parser.addoption(
        "--driver-path", type=str, action="store", default="", help="path to chrome driver",
    )
    parser.addoption(
        "--log-image-diffs", action="store_true", default=False,
        help="log image differences to result_images/image_diffs.log",
    )


def pytest_configure(config: pytest.Config) -> None:
    config.addinivalue_line("markers", "slow: mark test as slow to run")
    config.addinivalue_line("markers", "text: mark test as outputting text")
    config.addinivalue_line("markers", "image: mark test as generating comparison image")
    config.addinivalue_line("markers", "threads: mark test as using multiple threads")


def pytest_collection_modifyitems(config: pytest.Config, items: Sequence[Any]) -> None:
    if not config.getoption("--runslow"):
        skip_slow = pytest.mark.skip(reason="use --runslow option to run")
        for item in items:
            if "slow" in item.keywords:
                item.add_marker(skip_slow)

    if not config.getoption("--runtext"):
        skip_text = pytest.mark.skip(reason="use --runtext option to run")
        for item in items:
            if "text" in item.keywords and item.callspec.getparam("show_text"):
                item.add_marker(skip_text)


def pytest_make_parametrize_id(config: pytest.Config, val: Any, argname: str) -> str | None:
    # Override names used for enums in tests.
    if isinstance(val, FillType | LineType | ZInterp):
        return val.name
    return None


@pytest.fixture(scope="session")
def driver_path(request: SubRequest) -> Any:
    return request.config.getoption("--driver-path")
