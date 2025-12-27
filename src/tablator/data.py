"""
Table data handling functions
"""

import os

from tablator.logger import debug, trace

# Data directory (aka DATA_DIR)
_data_dir = None

# Table Name list cache
_table_list = None

def is_table(table_name=None):
    """
    Search DATA_DIR for a file called 'table_name.json' or 'table_name.yaml'.
    Returns True if found, False is not
    """
    trace('is_table')
    if table_name is None:
        raise ValueError('table_name is None')
    global _table_list

    load_table_list()

    return table_name in _table_list


def list_tables(*args):
    """
    Return a list of tables in DATA_DIR.
    Any file in DATA_DIR with a json or yaml extension is considered to be
    a table.
    """
    trace('list_tables')
    load_table_list()
    return list(_table_list)


def load(table_name=None):
    """
    Load a table from DATA_DIR, return Python.
    """
    trace('load')
    if table_name is None:
        raise ValueError('table_name is None')

    table_file = os.path.join(_data_dir, table_name + '.json')
    if os.path.exists(table_file):
        import json
        with open(table_file, 'r') as f:
            return json.load(f)

    table_file = os.path.join(_data_dir, table_name + '.yaml')
    if os.path.exists(table_file):
        import yaml
        with open(table_file, 'r') as f:
            return yaml.load(f, Loader=yaml.SafeLoader)

    raise ValueError("Table not found: " + table_name)


def load_table_list():
    """
    Build of list of table names from files in DATA_DIR with json or yaml
    extensions.
    """
    trace('load_table_list')
    global _data_dir, _table_list

    # List of Tables already exists, nothing to do
    if _table_list is not None:
        return

    # Build the list of tables
    table_list = list()

    for file_name in os.listdir(_data_dir):
        debug('file_name', file_name)
        if file_name.endswith('.json'):
            table_name = file_name.removesuffix('.json')
            table_list.append(table_name)
        elif file_name.endswith('.yaml'):
            table_name = file_name.removesuffix('.yaml')
            table_list.append(table_name)

    _table_list = sorted(table_list)


def set_data_dir(data_dir):
    """
    Set the data directory (DATA_DIR)
    Raises FileNotFoundError
    """
    trace('set_data_dir')
    data_dir = os.path.realpath(data_dir)
    if os.path.isdir(data_dir):
        debug('Setting DATA_DIR to', data_dir)
        global _data_dir
        _data_dir = data_dir
    else:
        raise FileNotFoundError(data_dir)
