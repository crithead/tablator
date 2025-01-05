#!/usr/bin/env python3
# Read a CSV file and output a JSON "items" table.
#
# Note: The default field separator is '\t' (not ',')
#
# Input format 1:
# name
#
# Input format 2:
# weight // name
#
# Input format 3:
# min // max // name
#
# Input format 4:
# name // subtable
#
# Input format X: TODO
# weight // name // subtable // value // quantity
# min // max // name // subtable // value // quantity
#

import argparse
import csv
import json
import os.path

def get_args():
    parser = argparse.ArgumentParser(
        description='Convert CSV files to Tablator item tables in JSON',
        epilog='Valid header items: name, min, max, weight, subtable, value' +
            ', quantity')

    parser.add_argument('-D', '--output-dir', action='store', default=None,
        help='directory to put the output json files in')
    parser.add_argument('-n', '--table-name', action='store', default=None,
        help='the table name (applied to all tables)')
    #parser.add_argument('-d', '--debug', action='store_true', default=False,
    #    help='enable debugging messages')
    #parser.add_argument('-v', '--verbose', action='store_true', default=False,
    #    help='enable information messages')
    parser.add_argument('csvfiles', nargs='+', help='Input CSV files')

    return parser.parse_args()


def read_csv(csv_file):
    rows = list()
    table = {
        'name': os.path.basename(csv_file),
        'type': 'items',
        'total-weight': 0,
        'rows': rows
    }

    with open(csv_file, newline='') as f:
        csvreader = csv.reader(f, delimiter='\t', quotechar='"')
        header = parse_header(next(csvreader))
        row_handler = get_row_handler(header)
        total_weight = 0
        for line in csvreader:
            row = row_handler(line)
            #if 'weight' in row:
            #    total_weight += int(row['weight'])
            #else:
            #    total_weight += 1
            total_weight += int(row['weight']) if 'weight' in row else 1
            rows.append(row)

    table['total-weight'] = total_weight

    return table


def parse_header(first_line):
    """
        Returns a dictionary of header fields.
    """
    # Convert to a list of lowercase strings
    items = list()
    for item in first_line:
        items.append(str(item).strip().lower())

    header = dict()
    if 'name' in items:
        header['name'] = True
    else:
        raise ValueError('Invalid header')
    if 'weight' in items:
        header['weight'] = True
    if 'min' in items and 'max' in items:
        header['min'] = True
        header['max'] = True
    if 'subtable' in items:
        header['subtable'] = True
    if 'value' in items:
        header['value'] = True
    if 'quantity' in items:
        header['quantity'] = True

    return header


def get_row_handler(header):
    if 'name' not in header:
        raise ValueError('Invalid header')
    if len(header) == 1:
        return parse_name_only
    if len(header) == 2:
        if 'weight' in header:
            return parse_weight_name
        if 'subtable' in header:
            return parse_name_subtable
    if len(header) == 3:
        if 'min' in header and 'max' in header:
            return parse_min_max_name
    raise ValueError('Invalid header')


def parse_name_only(line):
    return {
        'name': line[0]
    }


def parse_weight_name(line):
    return {
        'name': line[1],
        'weight': int(line[0])
    }


def parse_name_subtable(line):
    return {
        'name': line[0],
        'subtable': line[1]
    }


def parse_min_max_name(line):
    weight = int(line[1]) - int(line[0]) + 1
    return {
        'name': line[2],
        'weight': weight
    }


def get_output_file(input_file, output_dir=None):
    output_file = 'item-table.json'

    if output_dir is None:
        output_file = input_file
    else:
        output_file = os.path.join(output_dir, os.path.basename(input_file))

    if output_file.endswith('.csv'):
        output_file = output_file.replace('.csv', '.json')
    else:
        output_file += '.json'

    # TODO expand ~ and environment variables
    return output_file


def write_item_table(table, json_file):
    with open(json_file, 'w') as f:
        json.dump(table, f)


if __name__ == '__main__':
    exit_code = None

    try:
        args = get_args()

        for csv_file in args.csvfiles:
            table = read_csv(csv_file)
            json_file = get_output_file(csv_file, args.output_dir)
            if args.table_name is not None:
                table['name'] = args.table_name
            write_item_table(table, json_file)

        exit_code = 0
    except Exception as e:
        import traceback
        traceback.print_exc()
        #print(e)
        exit_code = 1
    finally:
        if exit_code is None:
            print("Warning: exit_code is None")
            exit_code = 99
    exit(exit_code)

