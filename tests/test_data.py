# Unit t  ests for tablator.data functions.

import os
import pytest
import tablator.data as data

def test_is_table_yes(monkeypatch):
    def mock_os_listdir(dir_name):
        return ['shiny-things.yaml', 'sparkly-things.json']

    monkeypatch.setattr(os, "listdir", mock_os_listdir)
    assert data.is_table('shiny-things') is True
    assert data.is_table('sparkly-things') is True


def test_is_table_no(monkeypatch):
    def mock_os_listdir(dir_name):
        return ['shiny-things.yaml', 'sparkly-things.json']

    monkeypatch.setattr(os, "listdir", mock_os_listdir)
    assert data.is_table('shady-things') is False


def test_is_table_no_table_name():
    with pytest.raises(ValueError, match=r'table_name is None'):
        data.is_table()
    with pytest.raises(ValueError, match=r'table_name is None'):
        data.is_table(None)


def test_list_tables_no_dir(monkeypatch):
    def mock_listdir(dir_name):
        return list()

    monkeypatch.setattr(os, 'listdir', mock_listdir)
    table_list = data.list_tables()
    assert len(table_list) == 0


def test_list_tables_empty(monkeypatch):
    def mock_listdir(dir_name):
        return list()

    monkeypatch.setattr(os, 'listdir', mock_listdir)
    table_list = data.list_tables()
    assert len(table_list) == 0


def test_list_tables_1(monkeypatch):
    def mock_listdir(dir_name):
        return [ 'table-one.json', 'table-two.yaml' ]

    monkeypatch.setattr(os, 'listdir', mock_listdir)
    tables = data.list_tables()
    assert tables == [ 'table-one', 'table-two' ]


def test_load_table_name_is_none():
    with pytest.raises(ValueError, match='table_name is None'):
        data.load(None)


def test_load_table_name_doesnt_exist():
    with pytest.raises(ValueError, match='Table not found: not-a-table'):
        data.load('not-a-table')


def test_load_json_table():
    data.DATA_DIR = os.path.realpath(os.path.join('.', 'tests'))
    table = data.load('table-j')
    print(table)


def test_load_yaml_table():
    data.DATA_DIR = os.path.realpath(os.path.join('.', 'tests'))
    table = data.load('table-y')
    print(table)


def test_set_data_dir_exists():
    this_dir = os.path.realpath('.')
    data.set_data_dir('.')
    assert data.DATA_DIR == this_dir


def test_set_data_dir_doesnt_exist():
    with pytest.raises(FileNotFoundError, match='/does/not/exist'):
        data.set_data_dir('/does/not/exist')

