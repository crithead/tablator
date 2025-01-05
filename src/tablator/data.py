"""
Table data handling functions
"""

import os

from tablator.logger import debug, trace

# Default data directory when installed
DEFAULT_DATA_DIR = '/usr/share/tablator-data'

# Data directory (contains table definitions)
DATA_DIR = DEFAULT_DATA_DIR


def is_table(table_name=None):
    """
    Search DATA_DIR for a file called 'table_name.json' or 'table_name.yaml'.
    Returns True if found, False is not
    """
    trace('is_table')
    if table_name is None:
        raise ValueError('table_name is None')

    for file_name in os.listdir(DATA_DIR):
        debug('file_name', file_name)
        if file_name == table_name + '.yaml':
            debug('found: ', DATA_DIR, '/', file_name)
            return True
        if file_name == table_name + '.json':
            debug('found: ', DATA_DIR + '/' + file_name)
            return True
    debug('not found: ', table_name, 'in', DATA_DIR)
    return False


def list_tables(*args):
    """
    Return a list of tables in DATA_DIR.
    Any file in DATA_DIR with a json or yaml extension is considered to be
    a table.
    """
    trace('list_tables')
    files = list()
    for file_name in os.listdir(DATA_DIR):
        parts = file_name.split('.')
        if parts[-1] == 'json' or parts[-1] == 'yaml':
            files.append('.'.join(parts[:-1]))
    return files


def load(table_name=None):
    """
    Load a table from DATA_DIR, return Python.
    """
    trace('load')
    if table_name is None:
        raise ValueError('table_name is None')

    table_file = os.path.join(DATA_DIR, table_name + '.json')
    if os.path.exists(table_file):
        import json
        with open(table_file, 'r') as f:
            return json.load(f)

    table_file = os.path.join(DATA_DIR, table_name + '.yaml')
    if os.path.exists(table_file):
        import yaml
        with open(table_file, 'r') as f:
            return yaml.load(f, Loader=yaml.SafeLoader)

    raise ValueError("Table not found: " + table_name)


def set_data_dir(data_dir):
    """
    Set the data directory (DATA_DIR)
    Raises FileNotFoundError
    """
    trace('set_data_dir')
    data_dir = os.path.realpath(data_dir)
    if os.path.isdir(data_dir):
        debug('Setting DATA_DIR to', data_dir)
        global DATA_DIR
        DATA_DIR = data_dir
    else:
        raise FileNotFoundError(data_dir)
