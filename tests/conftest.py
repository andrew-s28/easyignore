import os
from pathlib import Path

import pytest


def pytest_configure(config):
    # required to make sure files are created in the same directory as the test file
    os.chdir(Path(__file__).parent.resolve())


@pytest.fixture(autouse=True)
def setup_and_teardown():
    # Setup code
    yield
    # Teardown code
    for path in Path(__file__).resolve().parent.iterdir():
        print(path)
        if path.name.endswith(".gitignore"):
            path.unlink()
        elif path.name.endswith(".prettierignore"):
            path.unlink()
