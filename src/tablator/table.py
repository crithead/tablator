"""
Table operations
"""

import re
from random import randint

import tablator.data
from tablator.logger import debug, trace

# Cache loaded tables (dict of 'name': str, 'table': dict)
_tables = dict()


def check_weights(table):
    """
    Check that row weights add up to total-weight.
    Raise ValueError if not equal
    """
    trace('check_weights')
    if 'total-weight' not in table:
        raise ValueError(f'{table} has no "total-weight" key')

    total_weight = table['total-weight']
    weight_total = 0
    if 'rows' in table:
        for row in table['rows']:
            row_weight = row['weight'] if 'weight' in row else 1
            weight_total += row_weight
        debug('table', table['name'], 'weight', weight_total, 'of', total_weight)
        if total_weight != weight_total:
            raise ValueError("{}: row weights don't add up: {} of {}".
                             format(table['name'], weight_total, total_weight))
    elif 'columns' in table:
        weight_total = len(table['columns'])
        if total_weight != weight_total:
            raise ValueError(f"{table}: columns count doesn't add up: {weight_total} of {total_weight}")
    else:
        raise ValueError(f'Invalid table: {table}')


def generate(table_name, num_rolls=1):
    """
    Generate N items from the given table.
    Assumes DATA_DIR has been set.
    Return a list of item names (str).
    Raises ValueError if the table cannot be loaded.
    """
    trace('generate')

    table = load_table(table_name)

    values = list()
    if 'rows' in table:
        for i in range(num_rolls):
            item_name = lookup_rows(table)
            values.append(item_name)
    elif 'columns' in table:
        for i in range(num_rolls):
            item_list = lookup_columns(table)
            values.extend(item_list)
    else:
        raise ValueError('Invalid table: missing rows or columns key')

    return values


def get_chance(column):
    """
    Get the optional chance value from a tables column.
    Default is 100, if not present.
    Raises ValueError if out of range.
    :param column: dict
    :return: number in [1, 100]
    """
    trace('get_chance')
    value = 100
    if 'chance' in column:
        chance = column['chance']
        if 0 < chance and chance <= 100:
            value = chance
        else:
            raise ValueError(f'Column chance out of range: {chance}')
    return value


def get_table_name(table_name):
    """
    Returns a table's name (value from 'name' key)
    Raises ValueError if the table cannot be loaded.
    :table_name: table's file name
    """
    return load_table(table_name)['name']


def load_table(table_name):
    """
    Load a table from a file, cache the result.
    Returns a table (dict)
    Raises ValueError
    """
    global _tables

    trace('load_table')
    table = None
    if table_name in _tables:
        table = _tables[table_name]
        debug('cache hit', table_name)
    else:
        table = tablator.data.load(table_name)
        check_weights(table)
        _tables[table_name] = table
        debug('loaded', table_name)

    return table


def lookup_rows(table):
    """
    Do a lookup in an row table, return the result.
    Returns a string.
    Raises ValueError.
    """
    trace('lookup_rows')
    debug('lookup_rows', table['name'], table['total-weight'],
          len(table['rows']))
    item = random_row(table)
    if 'table' in item:
        subtable = load_table(item['table'])
        return lookup_rows(subtable)
    item_name = item['name']
    subitem = None
    quantity = None
    units = None
    if 'subtable' in item:
        debug('roll on subtable', item['subtable'])
        subtable = load_table(item['subtable'])
        if 'rows' in subtable:
            subitem = lookup_rows(subtable)
        elif 'columns' in subtable:
            subitem = lookup_columns(subtable)
            if len(subitem) > 1:
                subitem = ', '.join(subitem)
            else:
                subitem = subitem[0]
        else:
            raise ValueError(f"Invalid subtable: {item['subtable']}")
        # if len(subitem) == 0:
        #     subitem = None
    if 'quantity' in item:
        debug('roll quantity', item['quantity'])
        quantity = roll_quantity(item['quantity'])
        if 'units' in item:
            quantity = f'{quantity} {item["units"]}'
        if quantity == '1':
            quantity = None

    if subitem is not None and quantity is not None:
        item_name = '{} ({}, {})'.format(item['name'], subitem, quantity)
    elif subitem is not None:
        item_name = '{} ({})'.format(item['name'], subitem)
    elif quantity is not None:
        item_name = '{} ({})'.format(item['name'], quantity)
    else:
        item_name = '{}'.format(item['name'])
    return item_name


def lookup_columns(table):
    """
    The top-level table is a list of tables.
    Roll once on each table in the list.
    Returns a list of item names.
    Each table column has:
        name: the name of the item or table
        chance: roll less than or equal to this value for item to be generated
        table: if None, use "quantity + name", else roll on table
        quantity: number of items (bunch) or rolls on table
    """
    trace('lookup_columns')
    debug('table name', table['name'])
    values = list()
    columns = table['columns']
    for column in columns:
        chance = get_chance(column)
        roll = randint(1, 100)
        if roll > chance:
            if 'name' in column:
                debug('skip', column['name'], roll, 'vs', column['chance'])
            else:
                debug('skip', column['table'], roll, 'vs', column['chance'])
            continue    # failed chance roll
        if 'table' in column:
            quantity = roll_quantity(column['quantity']) if 'quantity' in column else 1
            table_name = column['table']
            for i in range(int(quantity)):
                debug('rolling on table', table_name)
                subtable = load_table(table_name)
                if 'rows' in subtable:
                    item_name = lookup_rows(subtable)
                    values.append(item_name)
                elif 'columns' in subtable:
                    item_list = lookup_columns(subtable)
                    values.extend(item_list)
                else:
                    raise ValueError('invalid table type: ' + subtable['type'])
        else:  # use name 
            quantity = roll_quantity(column['quantity'])
            name = column['name']
            values.append('{} {}'.format(quantity, name))
    return values


def print_plain(table_name):
    """
    Print a table as plain text to the standard output.
    """
    trace('print_plain')
    table = load_table(table_name)
    index = 1
    if 'rows' in table:
        # A table of items
        debug('print "rows" table')
        dice = str(table['total-weight'])
        if dice == '100': dice = '%'
        print(' d{}'.format(dice), table['name'], sep='\t')
        print('-----', '-' * len(table['name']), sep='\t')
        for row in table['rows']:
            wt = row['weight'] if 'weight' in row else 1
            row_name = row['name'] if 'name' in row else get_table_name(row['table'])
            if 'quantity' in row:
                if 'units' in row:
                    row_name += ' ({} {})'.format(row['quantity'], row['units'])
                else:
                    row_name += ' ({})'.format(row['quantity'])
            s = None
            if wt > 1:
                s = "{:02d}-{:02d}\t{}".format(index, index + wt - 1, row_name)
            else:
                s = "{:02d}\t{}".format(index, row_name)
            index += wt
            print(s)
        print()
    elif 'columns' in table:
        # A list of tables, roll on each table
        debug('print "columns" table')
        print(table['name'])
        print('-' * len(table['name']))
        for column in table['columns']:
            chance = '{0:3d}%'.format(get_chance(column))
            quantity = column['quantity'] if 'quantity' in column else '1'
            if 'name' in column:
                name = column['name']
            elif 'table' in column and column['table'] is not None:
                name = get_table_name(column['table'])
            else:
                raise ValueError('invalid column: no name or table')
            if quantity == '1':
                print(chance, name)
            else:
                print(chance, quantity, name)
        print()

    else:
        debug('Malformed table')


def random_row(table):
    """
    Return a random row dict from a table.
    """
    trace('random_row')
    total_weight = table['total-weight']
    item_index = randint(1, total_weight)
    weight_total = 0
    for row in table['rows']:
        row_weight = row['weight'] if 'weight' in row else 1
        weight_total += row_weight
        if weight_total >= item_index:
            return row
    raise RuntimeError('row index out of bounds: index {}, total_weight {}'
                       .format(item_index, total_weight))


#   1       10
#   1d6     1d6x10
#   2d6-1
#   2d10+3x100
#           IdJ+KxM = (number)d(sides)(+/-adjustment)x(multiplier)
PATTERN = '([1-9][0-9]*)d([1-9][0-9]*)([+-][1-9][0-9]*)?(?:x([1-9][0-9]*))?'
MATCHER = re.compile(PATTERN)


def roll_quantity(quantity):
    """
    Roll some dice
    "3d6+6x10" -> ((3 x 1-6) + 6) x 10 -> 160
    """
    trace("roll_quantity")
    result = MATCHER.fullmatch(quantity)
    if result is None:
        debug('no match', quantity)
        value = quantity
    else:
        groups = result.groups()
        number = int(groups[0])
        sides = int(groups[1])
        if groups[2] is not None:
            adjustment = int(groups[2])
        else:
            adjustment = 0
        if groups[3] is not None:
            multiplier = int(groups[3])
        else:
            multiplier = 1

        debug('number', number, 'sides', sides, 'adjustment', adjustment,
              'multiplier', multiplier)

        n = 0
        for i in range(number):
            n += randint(1, sides)

        value = (n + adjustment) * multiplier

    debug('value', value)
    return str(value)
