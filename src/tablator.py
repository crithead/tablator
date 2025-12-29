#!/usr/bin/env python3
"""
Treasure Table -- Generate
"""

import argparse
import os
import sys
import traceback

import tablator
import tablator.logger


def apply_environ(args):
    """
    Fill in missing argument values from the environement.
    Options: data_dir
    """
    if args.trace: print('=== apply_environ')

    if args.data_dir is None and 'TABLATOR_DATA_DIR' in os.environ:
        args.data_dir = os.environ['TABLATOR_DATA_DIR']
        if args.verbose:
            print(f'--- Found TABLATOR_DATA_DIR = {args.data_dir}')


def check_data_dir(args):
    """
    Check DATA_DIR.
    Set to PWD if None.
    Riase ValeError is non-existent.
    """
    tablator.logger.trace('check_data_dir')

    if args.data_dir is None:
         args.data_dir = os.getcwd()

    if os.path.isdir(args.data_dir):
        tablator.logger.debug(f'Using DATA_DIR = {args.data_dir}')
    else:
        raise ValueError(f'DATA DIR ({args.data_dir}) does not exist')


def get_args():
    """
    Get command line arguments.
    """
    parser = argparse.ArgumentParser(
        description='Roll on a table',
        epilog='\n')
    parser.add_argument('-d', '--data-dir', action='store', default=None,
                        help='let the table data directory')
    parser.add_argument('-l', '--list', action='store_true', default=False,
                        help='list available tables')
    parser.add_argument('-n', '--number', action='store', default=1, type=int,
                        help='number of rolls on each table')
    parser.add_argument('-p', '--print', action='store_true', default=False,
                        help='print the table (plain text)')
    parser.add_argument('-t', '--trace', action='store_true', default=False,
                        help='enable trace messages')
    parser.add_argument('-v', '--verbose', action='store_true', default=False,
                        help='enable debug messages')
    parser.add_argument('tables', nargs='*',
                        help='table names')
    return parser.parse_args()


if __name__ == '__main__':
    exit_code = None
    try:
        args = get_args()
        apply_environ(args)
        tablator.logger.set(args.verbose, args.trace)

        check_data_dir(args)
        tablator.set_data_dir(args.data_dir)

        if args.list:
            table_list = tablator.data.list_tables()
            print('', 'Available tables', '', sep='\n')
            for table_name in sorted(table_list):
                print('   ', table_name)
            print()
            exit_code = 0

        else:  # do table lookups
            exit_code = 1
            for table_name in args.tables:
                if args.print:
                    tablator.print_plain(table_name)
                else:
                    items = tablator.generate(table_name, args.number)
                    for item in items:
                        print(item)
                exit_code = 0

    except ValueError as e:
        traceback.print_exc()
        print(repr(e), file=sys.stderr)
        exit_code = 1

    except Exception:
        traceback.print_exc()
        exit_code = 1

    finally:
        if exit_code is None:
            print('Warning: exit_code is None', file=sys.stderr)
            exit_code = 99
        exit(exit_code)
