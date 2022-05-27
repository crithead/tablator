# Unit tests for tablator.data functions.

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


def test_list_tables_1():
    # data.list_tables()
    assert True


def test_load_1():
    # data.load()
    assert True


def test_set_data_dir_1():
    # data.set_data_dir()
    assert True
