from __future__ import annotations

from typing import TYPE_CHECKING, Any, Sequence

import pytest

if TYPE_CHECKING:
    from _pytest.fixtures import SubRequest


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


@pytest.fixture(scope="session")
def driver_path(request: SubRequest) -> Any:
    return request.config.getoption("--driver-path")
