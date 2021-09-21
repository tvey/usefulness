import random

import pytest

from ..fooddata import FoodData, APIException


def test_instance_not_created_with_invalid_key():
    with pytest.raises(APIException):
        assert FoodData('abc123')


def test_instance_created_with_valid_key(valid_key):
    assert FoodData(valid_key)


def test_search_finds_and_returns_data(fd):
    query = 'potato'
    result = fd.search(query)
    assert result
    assert isinstance(result, list)


def test_search_returns_empty_result(fd):
    query = 'yumyumyum'
    result = fd.search(query)
    assert result == []


def test_search_handles_food_id(fd):
    query = 1097938
    result = fd.search(query)
    assert len(result) == 1


def test_search_with_empty_query_raises_error(fd):
    with pytest.raises(ValueError):
        assert fd.search('')


def test_search_with_bad_query_gracefully_returns_empty_list(fd):
    query = [1, 2, 3, 4]
    result = fd.search(query)
    assert result == []


def test_get_ids_retuns_expected_result(fd):
    result = fd.get_ids('banana')
    assert result
    assert all([isinstance(i, tuple) for i in result])
    food_id = random.choice(result)[0]
    food_name = random.choice(result)[1]
    assert isinstance(food_id, int)
    assert isinstance(food_name, str)


def test_get_foods_with_valid_ids(fd):
    ids = [1097958, 1100940, 1102822]
    result = fd.get_foods(ids)
    assert len(result) == 3


def test_get_foods_with_valid_and_invalid_ids(fd):
    valid_ids = [1100699, 1101064, 1102783]
    invalid_ids = [123, 321, 90]
    result = fd.get_foods(valid_ids + invalid_ids)
    assert len(result) == 3


def test_get_foods_with_bad_arg_1(fd):
    with pytest.raises(TypeError) as e:
        assert fd.get_foods(['banana', '1750349'])

    assert 'must be numbers' in str(e.value)


def test_get_foods_with_bad_arg_2(fd):
    with pytest.raises(TypeError) as e:
        assert fd.get_foods({'id': 123})

    assert 'numbers or a list of numbers' in str(e.value)
