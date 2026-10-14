import warnings

import pytest

from rcfl import store_model

warnings.filterwarnings("ignore", message="Workbook contains no default style")


@pytest.fixture(scope="session")
def cfg():
    return store_model.load_config()
