#!/usr/bin/env python3
"""
Treasure Table -- Generate
"""

import argparse
import os
import sys
import traceback

import tablator.data
import tablator.logger
import tablator.table


def apply_config(args):
    """
    Fill in option defaults from config file
    Options: data-dir, verbose, trace
    """

    # First use ~/.ttrc
    user_config_file = os.path.join(os.path.expanduser('~'), '.ttrc')
    config = load_config(user_config_file)

    # Second use ./.ttrc
    local_config_file = os.path.join(os.getcwd(), '.ttrc')
    config.update(load_config(local_config_file))

    # Third use args.config
    if args.config is not None:
        args_config_file = os.path.join(os.getcwd(), args.config)
        config.update(load_config(args_config_file))

    # Use valid config keys
    if 'data-dir' in config and args.data_dir is None:
        args.data_dir = os.path.expanduser(config.pop('data-dir'))
    if 'trace' in config and args.trace is False:
        args.trace = to_bool(config.pop('trace'))
    if 'verbose' in config and args.verbose is False:
        args.verbose = to_bool(config.pop('verbose'))

    # Note: using print here since logger has not been configured yet
    # Print invalid config keys
    if 'list' in config and args.verbose:
        value = config.pop('list')
        print('---', 'Ignoring config.list', value)
    if 'number' in config and args.verbose:
        value = config.pop('number')
        print('---', 'Ignoring config.number', value)
    if 'print' in config and args.verbose:
        value = config.pop('print')
        print('---', 'Ignoring config.print', value)

    # Print unknown config keys
    if len(config) > 0:
        print('---', 'Unknown config keys')
        for key in config.keys():
            print('key')


def find_data_dir():
    """Find a DATA_DIR"""
    tablator.logger.trace('find_data_dir')

    # At one time it seemed like a good idea to search some default locations
    # for the DATA_DIR, but as more table sets were generated, they are now in
    # sub-directories of 'tablator-data' so this isn't very useful.

    # Check for ~/.local/share/tablator-data
    local_share_dir = os.path.join(os.path.expanduser('~'), '.local', 'share',
                                   'tablator-data')
    if os.path.isdir(local_share_dir):
        return local_share_dir

    # Check for DEFAULT_DATA_DIR
    if os.path.isdir(tablator.data.DEFAULT_DATA_DIR):
        return tablator.data.DEFAULT_DATA_DIR

    # Fall back to CWD
    return os.getcwd()


def get_args():
    """
    Get command line arguments.
    """
    parser = argparse.ArgumentParser(
        description='Roll on a table',
        epilog='\n')
    parser.add_argument('-c', '--config', action='store', default=None,
                        help='load configuration from this file')
    parser.add_argument('-d', '--data-dir', action='store', default=None,
                        help='let the table data directory')
    parser.add_argument('-l', '--list', action='store_true', default=False,
                        help='list available tables')
    parser.add_argument('-n', '--number', action='store', default=1, type=int,
                        help='number of rolls on the table')
    parser.add_argument('-p', '--print', action='store_true', default=False,
                        help='print the table (plain text)')
    parser.add_argument('-t', '--trace', action='store_true', default=False,
                        help='enable trace messages')
    parser.add_argument('-v', '--verbose', action='store_true', default=False,
                        help='enable debug messages')
    parser.add_argument('tables', nargs='*',
                        help='table names')
    return parser.parse_args()


def load_config(config_file):
    """
    Load configuration from file into a dictionary.
    File format:
        # Comment
        key = value
    """
    config = dict()
    if os.path.isfile(config_file):
        with open(config_file, 'r') as f:
            for line in f:
                if line.startswith('#'):
                    continue
                fields = line.split('=')
                if len(fields) != 2:
                    print('---', 'Invalid config line:', line)
                    continue
                key = fields[0].strip()
                value = fields[1].strip()
                config[key] = value
    return config


def to_bool(string):
    """Interpret a string as a boolean value."""
    if string.lower() in [ 'yes', 'true', 'on', '1', 'enable' ]:
        return True
    else:
        return False


if __name__ == '__main__':
    exit_code = None
    try:
        #import pdb; pdb.set_trace()
        args = get_args()
        apply_config(args)
        tablator.logger.set(args.verbose, args.trace)

        if args.data_dir is None:
            data_dir = find_data_dir()
            tablator.data.set_data_dir(data_dir)
        else:
            tablator.data.set_data_dir(args.data_dir)

        tablator.logger.debug('DATA_DIR', tablator.data.DATA_DIR)

        if args.list:
            table_list = tablator.data.list_tables()
            print('', 'Available tables', '', sep='\n')
            for table_name in sorted(table_list):
                print('   ', table_name)
            print()
            exit_code = 0

        else:
            exit_code = 1
            for table_name in args.tables:
                if tablator.data.is_table(table_name):
                    if args.print:
                        tablator.table.print_plain(table_name)
                    else:
                        items = tablator.table.generate(table_name,
                                                             args.number)
                        for item in items:
                            print(item)
                    exit_code = 0
                else:
                    raise ValueError("Bad table name: " + table_name)

    except Exception:
        traceback.print_exc()
        exit_code = 1

    finally:
        if exit_code is None:
            print('Warning: exit_code is None', file=sys.stderr)
            exit_code = 99
        exit(exit_code)
