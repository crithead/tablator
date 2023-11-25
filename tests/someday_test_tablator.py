# PyTest for the tablator CLI tool.

import importlib.machinery
import importlib.util
import pathlib
import pytest

# Import tablator.py
try:
    # TODO Fix this to import the program file instead of the
    #      module directory.
    script_dir = pathlib.Path(__file__).parent
    module_path = str(script_dir.joinpath('..', 'src'))
    #print('module_path', module_path)

    loader = importlib.machinery.SourceFileLoader('tablator', module_path)
    spec = importlib.util.spec_from_loader('tablator', loader)
    tablator = importlib.util.module_from_spec(spec)
    loader.exec_module(tablator)

except ImportError as e:
    print(e)


@pytest.fixture
def one_item_table():
     return {
        'name': 'One Item Table',
        'type': 'items',
        'total-weight': 1,
        'rows': [
            {
                'weight': 1,
                'name': 'only row'
            }
        ]
    }


def test_apply_config_1():
    assert False, 'not implemented'


def test_find_data_dir_1():
    assert False, 'not implemented'


def test_get_args_1():
    assert False, 'not implemented'


def test_load_config_1():
    assert False, 'not implemented'


def test_is_bool_lowercase_true():
    assert tablator.is_bool('yes') is True
    assert tablator.is_bool('true') is True
    assert tablator.is_bool('on') is True
    assert tablator.is_bool('1') is True
    assert tablator.is_bool('enable') is True


def test_is_bool_uppercase_true():
    assert tablator.is_bool('YES') is True
    assert tablator.is_bool('TRUE') is True
    assert tablator.is_bool('ON') is True
    assert tablator.is_bool('ENABLE') is True


def test_is_bool_mixedcase_true():
    assert tablator.is_bool('Yes') is True
    assert tablator.is_bool('True') is True
    assert tablator.is_bool('On') is True
    assert tablator.is_bool('Enable') is True
    assert tablator.is_bool('yEs') is True
    assert tablator.is_bool('tRuE') is True
    assert tablator.is_bool('oN') is True
    assert tablator.is_bool('eNaBlE') is True


