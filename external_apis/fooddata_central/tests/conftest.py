import os

import pytest
import dotenv

from ..fooddata import FoodData

dotenv.load_dotenv()


@pytest.fixture
def valid_key():
    return os.environ.get('API_KEY')


@pytest.fixture
def fd(valid_key):
    return FoodData(valid_key)
