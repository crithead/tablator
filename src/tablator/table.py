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
    if 'total-weight' in table:
        total_weight = table['total-weight']
        weight_total = 0
        for row in table['rows']:
            row_weight = row['weight'] if 'weight' in row else 1
            weight_total += row_weight
        debug('table', table['name'], 'weight', weight_total, 'of', total_weight)
        if total_weight != weight_total:
            raise ValueError("{}: row weights don't add up: {} of {}".
                             format(table['name'], weight_total, total_weight))
    else:
        debug('not a weighted table', table['name'])


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
    if table['type'] == 'items':
        for i in range(num_rolls):
            item_name = lookup_items(table)
            values.append(item_name)
    elif table['type'] == 'tables':
        for i in range(num_rolls):
            item_list = lookup_tables(table)
            values.extend(item_list)
    else:
        raise ValueError('Unknown table type: ' + table['type'])

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
            raise ValueError('Column chance out of range: {}'.format(chance))
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


def lookup_items(table):
    """
    Do a lookup in an 'items' table, return the result.
    Returns a string.
    Raises ValueError.
    """
    trace('lookup_item')
    debug('lookup_item', table['name'], table['total-weight'],
          len(table['rows']))
    item = random_row(table)
    if 'table' in item:
        subtable = load_table(item['table'])
        return lookup_items(subtable)
    item_name = item['name']
    subitem = None
    quantity = None
    units = None
    if 'subtable' in item:
        debug('roll on subtable', item['subtable'])
        subtable = load_table(item['subtable'])
        if subtable['type'] == 'items':
            subitem = lookup_items(subtable)
        else:
            raise ValueError('invalid table type: ' + subtable['type'])
        # if len(subitem) == 0:
        #     subitem = None
    if 'quantity' in item:
        debug('roll quantity', item['quantity'])
        quantity = roll_quantity(item['quantity'])
        if 'units' in item:
            quantity = '{} {}'.format(quantity, item['units'])
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


def lookup_tables(table):
    """
    The top-level table is a list of tables.
    Roll once on each table in the list.
    Returns a list of item names.
    Each table item has:
        name: the name of the item or table
        chance: roll less than or equal to this value for item to be generated
        table: if None, use "quantity + name", else roll on table
        quantity: number of items (bunch) or rolls on table
    """
    trace('lookup_tables')
    debug('table name', table['name'])
    values = list()
    columns = table['columns']
    for column in columns:
        chance = get_chance(column)
        roll = randint(1, 100)
        if roll > chance:
            debug('skip', column['name'], roll, 'vs', column['chance'])
            continue    # failed chance roll
        if column['table'] is None:
            quantity = roll_quantity(column['quantity'])
            name = column['name']
            values.append('{} {}'.format(quantity, name))
        else:
            quantity = roll_quantity(column['quantity'])
            table_name = column['table']
            for i in range(int(quantity)):
                debug('rolling on table', table_name)
                subtable = load_table(table_name)
                if subtable['type'] == 'items':
                    item_name = lookup_items(subtable)
                    values.append(item_name)
                elif subtable['type'] == 'tables':
                    item_list = lookup_tables(subtable)
                    values.extend(item_list)
                else:
                    raise ValueError('invalid table type: ' + subtable['type'])
    return values


def print_plain(table_name):
    """
    Print a table as plain text to the standard output.
    """
    trace('print_plain')
    table = load_table(table_name)
    index = 1
    if table['type'] == 'items':
        # A table of items
        debug('print "items" table')
        dice = str(table['total-weight'])
        if dice == '100': dice = '%'
        print(' d{}'.format(dice), table['name'], sep='\t')
        print('-----', '-' * len(table['name']), sep='\t')
        # TODO Include quantity, if present
        for row in table['rows']:
            wt = row['weight'] if 'weight' in row else 1
            s = None
            if wt > 1:
                s = "{:02d}-{:02d}\t{}".format(index, index + wt - 1, row['name'])
            else:
                s = "{:02d}\t{}".format(index, row['name'])
            index += wt
            print(s)
        print()
    elif table['type'] == 'tables':
        # A list of tables, roll on each table
        debug('print "tables" table')
        print(table['name'])
        print('-' * len(table['name']))
        for column in table['columns']:
            chance = '{0:3d}%'.format(get_chance(column))
            quantity = column['quantity']
            name = column['name']
            if 'table' in column and column['table'] is not None:
                name = get_table_name(column['table'])
            print(chance, quantity, name) # TODO Format
        print()

    else:
        debug('unknown table type', table['type'])


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
