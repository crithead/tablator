#!/usr/bin/env python3
"""
Ingest text (or CSV) and output a Tablator table in JSON (or YAML)

Text Input:
    line is item (or table) name

CSV Input: (tab separated only)
    name
    name\\tweight
    name\\tweight\\tquantity
    name\\tweight\\tquantity\\tsubtable
"""

import argparse
import json
import sys
import yaml

_debug_on = False
_messages_on = True

def debug(*args):
    '''Print debugging messsages, if enabled, to stderr'''
    if _debug_on:
        print(*args, file=sys.stderr)


def msg(*args):
    '''Print messages, if enabled, to stdout'''
    if _messages_on:
        print(*args)


TABLE_TYPES = [ 'row', 'column' ]

def get_options():
    parser = argparse.ArgumentParser(
        description='Text to Table -- create tablator tables from text files',
        epilog='  ---  ')
    parser.add_argument('-c', '--csv', action='store_true', default=False,
            help='input files are CSV')
    parser.add_argument('-t', '--table-type', action='store', default="row",
            type=str, help='set the table type (default: row)')
    parser.add_argument('-n', '--table-name', action='store', default="TABLE NAME",
            type=str, help='set the table name')
    parser.add_argument('-w', '--weights', action='store_true', default=False,
            help='include weights in table rows')
    parser.add_argument('-D', '--debug', action='store_true', default=False,
            help='print debugging messages')
    parser.add_argument('-q', '--quiet', action='store_true', default=False,
            help='disable messages')
    parser.add_argument('-y', '--yaml', action='store_true', default=False,
            help='output table in YAML (default is JSON)')
    #  parser.add_argument('-v', '--verbose', action='store_true', default=False,
    #          help='Enable messages')
    parser.add_argument('textfiles', nargs='+',
                    help='text files to convert to tables')
    return parser.parse_args()


def read_file(textfile):
    debug('read_file')
    with open(textfile, 'r') as f:
         return f.readlines()


def lines_to_table(lines, opts):
    debug('lines_to_table')
    total_weight = 0
    rows = list()
    for line in lines:
        line = line.strip()
        if opts.csv:
            fields = line.split('\t')
            if len(fields) == 0:
                debug('empty line')
            elif len(fields) == 1:
                # name
                row = {'name': fields[0] }
            elif len(fields) == 2:
                # name, weight
                row = {
                    "name": fields[0],
                    "weight": int(fields[1])
                }
            elif len(fields) == 3:
                # name, weight, quantity
                row = {
                    "name": fields[0],
                    "weight": int(fields[1]),
                    "quantity": fields[2]
                }
            elif len(fields) == 4:
                # name, weight, quantity, subtable
                row = {
                    "name": fields[0],
                    "weight": int(fields[1]),
                    "quantity": fields[2],
                    "subtable": fields[3]
                }
            else:
                # invalid file format is a fatal error
                raise ValueError('line with more than four fields')

        elif opts.weights:
            row  ={"name": line, "weight": 1}
        else:
            row = {"name": line}

        rows.append(row)
        if 'weight' in row:
            total_weight += int(row['weight'])
        else:
            total_weight += 1


    # Clean up rows by removing keys where quantity is 1
    # or weight is 1 (unless opt.weights is True)
    for row in rows:
        if 'quantity' in row.keys() and row['quantity'] == "1":
            del row['quantity']
        if not opts.weights and 'weight' in row.keys() and row['weight'] == 1:
            del row['weight']

    return {
        "name": opts.table_name,
        "total-weight": total_weight,
        "rows": rows
    }

def write_table_json(table, table_file):
        debug('write_table_json')
        with open(table_file, 'w') as f:
            print(json.dumps(table, indent=2), file=f)


def write_table_yaml(table, table_file):
        debug('write_table_yaml')
        with open(table_file, 'w') as f:
            print(yaml.dump(table), file=f)


def main(opts):
    global TABLE_TYPES

    if opts.table_type not in TABLE_TYPES:
         raise ValueError(f'Invalid table type: {opts.table_type}')

    for textfile in opts.textfiles:
        lines = read_file(textfile)
        debug(f'Read {len(lines)} lines from {textfile}')

        table = lines_to_table(lines, opts)

        if opts.yaml:
            suffix = '.yml'
        else:
            suffix = '.json'

        if textfile.endswith('.csv'):
            table_file = textfile.replace('.csv', suffix)
        elif textfile.endswith('.txt'):
            table_file = textfile.replace('.txt', suffix)
        else:
            table_file = textfile + suffix

        if opts.yaml:
            write_table_yaml(table, table_file)
        else:
            write_table_json(table, table_file)

#
# Top level script
#
if __name__ == '__main__':
    value = 255
    try:
        opts = get_options()
        if opts.debug:
            _debug_on = True
            debug('Debug output enabled')
        if opts.quiet:
            _messages_on = False
        value = main(opts)
    except ValueError as e:
         print(e, file=sys.stderr)
    except Exception as e:
        print(e)
        import traceback
        traceback.print_exc()
        value = 254
    finally:
        exit(value)
