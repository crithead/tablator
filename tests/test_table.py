# PyTest for tablator.table

import pytest
import tablator.table
import tablator.logger

@pytest.fixture
def one_item_table():
     return {
        'name': 'One Item Table',
        'type': 'items',
        'total-weight': 1,
        'rows': [
            {
                'weight': 1,
                'name': 'only row'
            }
        ]
    }

@pytest.fixture
def two_item_table():
     return {
        'name': 'Two Item Table',
        'type': 'items',
        'total-weight': 2,
        'rows': [
            { 'weight': 1, 'name': 'row one' },
            { 'weight': 1, 'name': 'row two' }
        ]
    }

@pytest.fixture
def default_weight_table():
     return {
        'name': 'Two Item Table',
        'type': 'items',
        'total-weight': 5,
        'rows': [
            { 'name': 'row one' },
            { 'name': 'row two' },
            { 'name': 'row three' },
            { 'name': 'row four' },
            { 'name': 'row five' }
        ]
    }

@pytest.fixture
def nine_item_table():
     return {
        'name': 'Nine Item Table',
        'type': 'items',
        'total-weight': 45,
        'rows': [
            { 'weight': 1, 'name': 'row one' },
            { 'weight': 2, 'name': 'row two' },
            { 'weight': 3, 'name': 'row three' },
            { 'weight': 4, 'name': 'row four' },
            { 'weight': 5, 'name': 'row five' },
            { 'weight': 6, 'name': 'row six' },
            { 'weight': 7, 'name': 'row seven' },
            { 'weight': 8, 'name': 'row eight' },
            { 'weight': 9, 'name': 'row nine' }
        ]
    }


@pytest.fixture
def one_subtable_table():
     return {
        'name': 'One Subtable Table',
        'type': 'items',
        'total-weight': 1,
        'rows': [
            {
                'weight': 1,
                'name': 'only subtable row',
                'subtable': 'one-item-table'
            }
        ]
    }


@pytest.fixture
def one_subtable_quantity_table():
     return {
        'name': 'One Subtable Table with Quantity',
        'type': 'items',
        'total-weight': 10,
        'rows': [
            {
                'weight': 10,
                'name': 'only subtable row',
                'subtable': 'one-item-table',
                'quantity': '20'
            }
        ]
    }


@pytest.fixture
def one_subtable_quantity_units_table():
     return {
        'name': 'One Subtable Table with Value',
        'type': 'items',
        'total-weight': 10,
        'rows': [
            {
                'weight': 10,
                'name': 'only subtable row',
                'subtable': 'one-item-table',
                'quantity': '1000',
                'units': 'widgets'
            }
        ]
    }


@pytest.fixture
def bad_weight_table():
     return {
        'name': 'Bad Weight Item Table',
        'type': 'items',
        'total-weight': 10,
        'rows': [
            { 'weight': 1, 'name': 'row one' },
            { 'weight': 3, 'name': 'row two' },
            { 'weight': 5, 'name': 'row three' },
            { 'weight': 3, 'name': 'row four' },
            { 'weight': 1, 'name': 'row five' }
        ]
    }


@pytest.fixture
def tables_table():
     return {
        'name': 'Tables Table',
        'type': 'tables',
        'total-weight': 50,
        'rows': [
            { 'weight': 25, 'table': 'one-item-table' },
            { 'weight': 25, 'table': 'two-item-table' }
        ]
    }


@pytest.fixture
def table_list():
     return {
        'name': 'Table List',
        'type': 'table-list',
        'columns': [
            {
                'chance': 50,
                'name': 'First Table',
                'quantity': '1',
            },
            {
                'chance': 80,
                'name': 'Second Table',
                'table': None,
                'quantity': '1',
            },
            {
                'chance': 35,
                'name': 'Third Table',
                'quantity': '2',
                'table': 'two-item-table'
            },
        ]
    }


@pytest.fixture
def table_list_no_chance():
     return {
        'name': 'Table List, No Chance',
        'type': 'table-list',
        'columns': [
            {
                'name': 'First Table',
                'quantity': '1'
            },
            {
                'name': 'Second Table',
                'quantity': '2d10'
            },
        ]
    }


@pytest.fixture
def table_list_bad_chance():
     return {
        'name': 'Table List, Bad Chance',
        'type': 'table-list',
        'columns': [
            {
                'name': 'First Table',
                'chance': -99,
                'table': 'one-item-table'
            },
            {
                'name': 'Second Table',
                'chance': 1234,
                'table': 'one-item-table'
            },
        ]
    }


@pytest.fixture
def unknown_table():
     return {
        'name': 'One Item Table',
        'type': 'unknown',
    }


def test_check_weights_1(one_item_table):
    try:
        tablator.table.check_weights(one_item_table)
    except ValueError as e:
        assert False, f'unexpected exception: {e}'


def test_check_weights_2(nine_item_table):
    try:
        tablator.table.check_weights(nine_item_table)
    except ValueError as e:
        assert False, f'unexpected exception: {e}'


def test_check_weights_default_weights(default_weight_table):
    try:
        tablator.table.check_weights(default_weight_table)
    except ValueError as e:
        assert False, f'unexpected exception: {e}'


def test_check_weights_non_weighted(capsys, table_list):
    tablator.logger.set(True, False)    # enable debug output
    tablator.table.check_weights(table_list)
    tablator.logger.set(False, False)   # disable debug output
    out, err = capsys.readouterr()
    #with capsys.disabled():
    #    print('out', out, sep='\n')
    assert out.startswith('--- not a weighted table')


def test_check_weights_bad_weights(bad_weight_table):
    with pytest.raises(ValueError, match=r".* row weights don't add up: .*"):
        tablator.table.check_weights(bad_weight_table)


def test_generate_invalid_table(monkeypatch):
    def mock_load_table(table_name):
        return None

    with pytest.raises(ValueError, match='Table not found: no-table'):
        tablator.table.generate('no-table', 1)


def test_generate_item_table(monkeypatch, one_item_table):
    def mock_load_table(table_name):
        return one_item_table

    monkeypatch.setattr(tablator.table, 'load_table', mock_load_table)
    values = tablator.table.generate('one-item-table', 3)
    assert values == ['only row', 'only row', 'only row']


def test_generate_table_list_table(monkeypatch, one_item_table):
    def mock_load_table(table_name):
        return one_item_table

    def mock_lookup_table_list(table_name):
        return ['only row']

    monkeypatch.setattr(tablator.table, 'load_table', mock_load_table)
    monkeypatch.setattr(tablator.table, 'lookup_table_list', mock_lookup_table_list)
    values = tablator.table.generate('list-table', 3)
    assert values == ['only row', 'only row', 'only row']


def test_generate_tables_table(monkeypatch, one_item_table):
    def mock_load_table(table_name):
        return one_item_table

    def mock_lookup_tables(table_name):
        return ['only row']

    monkeypatch.setattr(tablator.table, 'load_table', mock_load_table)
    monkeypatch.setattr(tablator.table, 'lookup_tables', mock_lookup_tables)
    values = tablator.table.generate('tables-table', 2)
    assert values == ['only row', 'only row']


    #tablator.table.generate(table_name, num_rolls=1)
    assert True


def test_generate_invalid_table_type(monkeypatch, unknown_table):
    def mock_load_table(table_name):
        return unknown_table

    monkeypatch.setattr(tablator.table, 'load_table', mock_load_table)
    with pytest.raises(ValueError, match='Unknown table type: unknown'):
        tablator.table.generate('unknown-table', 1)


def test_get_chance_not_present(table_list_no_chance):
    chance = tablator.table.get_chance(table_list_no_chance['columns'][0])
    assert chance == 100
    chance = tablator.table.get_chance(table_list_no_chance['columns'][1])
    assert chance == 100


def test_get_chance_invalid_chance(table_list_bad_chance):
    with pytest.raises(ValueError, match='Column chance out of range: -99'):
        chance = tablator.table.get_chance(table_list_bad_chance['columns'][0])
    with pytest.raises(ValueError, match='Column chance out of range: 1234'):
        chance = tablator.table.get_chance(table_list_bad_chance['columns'][1])


def test_get_chance_ok(table_list):
    chance = tablator.table.get_chance(table_list['columns'][0])
    assert chance == 50
    chance = tablator.table.get_chance(table_list['columns'][1])
    assert chance == 80
    chance = tablator.table.get_chance(table_list['columns'][2])
    assert chance == 35


def test_get_table_name_ok(monkeypatch, one_item_table):
    def mock_load_table(table_name):
        return one_item_table

    monkeypatch.setattr(tablator.table, 'load_table', mock_load_table)
    name = tablator.table.get_table_name('one-item-table')
    assert name == 'One Item Table'
    assert name == one_item_table['name']


def test_get_table_name_no_name(monkeypatch):
    def mock_load_table(table_name):
        return dict()

    monkeypatch.setattr(tablator.table, 'load_table', mock_load_table)
    with pytest.raises(KeyError):
        chance = tablator.table.get_table_name('empty-table')


def test_load_table_cache_miss(capsys, monkeypatch, one_item_table):
    def mock_load(table_name):
        return one_item_table

    tablator.table._tables.clear()      # clear the table cache
    tablator.logger.set(True, False)    # enable debug output
    monkeypatch.setattr(tablator.data, 'load', mock_load)
    table = tablator.table.load_table('one-item-table')
    tablator.logger.set(False, False)   # disable debug output
    out, err = capsys.readouterr()
    assert '--- loaded one-item-table' in out
    assert table is not None


def test_load_table_cache_hit(capsys, monkeypatch, one_item_table):
    def mock_load(table_name):
        return one_item_table

    tablator.table._tables.clear()      # clear the table cache
    tablator.logger.set(False, False)   # disable debug output
    monkeypatch.setattr(tablator.data, 'load', mock_load)
    # Call once to load the table cache
    table = tablator.table.load_table('one-item-table')
    tablator.logger.set(True, False)    # enable debug output
    # Now get table from the table cache
    table = tablator.table.load_table('one-item-table')
    tablator.logger.set(False, False)   # disable debug output
    out, err = capsys.readouterr()
    assert '--- cache hit one-item-table' in out
    assert table is not None


def test_lookup_items_simple_lookup(monkeypatch, one_item_table):
    def mock_random_row(table_name):
        return { 'name': 'fake row' }

    monkeypatch.setattr(tablator.table, 'random_row', mock_random_row)
    item_name = tablator.table.lookup_items(one_item_table)
    assert item_name == 'fake row'


def test_lookup_items_quantity(monkeypatch, one_item_table):
    def mock_random_row(table_name):
        return { 'name': 'fake row', 'quantity': '10' }

    monkeypatch.setattr(tablator.table, 'random_row', mock_random_row)
    item_name = tablator.table.lookup_items(one_item_table)
    assert item_name == 'fake row (10)'


def test_lookup_items_subtable(monkeypatch, one_subtable_table, one_item_table):
    def mock_random_row(table):
        if table is one_subtable_table:
            return one_subtable_table['rows'][0]
        if table is one_item_table:
            return one_item_table['rows'][0]
        assert False, 'Invalid table!'

    def mock_load_table(table_name):
        return one_item_table

    monkeypatch.setattr(tablator.table, 'random_row', mock_random_row)
    monkeypatch.setattr(tablator.table, 'load_table', mock_load_table)
    item_name = tablator.table.lookup_items(one_subtable_table)
    assert item_name == 'only subtable row (only row)'


def test_lookup_items_subtable_quantity(monkeypatch, one_item_table,
                                        one_subtable_quantity_table):
    def mock_random_row(table):
        if table is one_subtable_quantity_table:
            return one_subtable_quantity_table['rows'][0]
        if table is one_item_table:
            return one_item_table['rows'][0]
        assert False, 'Invalid table!'

    def mock_load_table(table_name):
        return one_item_table

    monkeypatch.setattr(tablator.table, 'random_row', mock_random_row)
    monkeypatch.setattr(tablator.table, 'load_table', mock_load_table)
    item_name = tablator.table.lookup_items(one_subtable_quantity_table)
    assert item_name == 'only subtable row (only row, 20)'


def test_lookup_items_subtable_quantity_units(monkeypatch, one_item_table,
                                     one_subtable_quantity_units_table):
    def mock_random_row(table):
        if table is one_subtable_quantity_units_table:
            return one_subtable_quantity_units_table['rows'][0]
        if table is one_item_table:
            return one_item_table['rows'][0]
        assert False, 'Invalid table!'

    def mock_load_table(table_name):
        return one_item_table

    monkeypatch.setattr(tablator.table, 'random_row', mock_random_row)
    monkeypatch.setattr(tablator.table, 'load_table', mock_load_table)
    item_name = tablator.table.lookup_items(one_subtable_quantity_units_table)
    assert item_name == 'only subtable row (only row, 1000 widgets)'


def test_lookup_table_list():
    #tablator.table.lookup_table_list(table)
    assert True


def test_lookup_tables():
    #tablator.table.lookup_tables(table)
    assert True


# * Mock load_table('table-name')
# * Capture sys.stdout and compare
def test_print_plain_item_table(capsys, monkeypatch, one_item_table):
    def mock_load_table(table_name):
        return one_item_table

    monkeypatch.setattr(tablator.table, "load_table", mock_load_table)
    tablator.table.print_plain('one-item-table')
    out, err = capsys.readouterr()
    #with capsys.disabled():
    #    print('out', out, sep='\n')
    assert out == '''\
 d1	One Item Table
-----	--------------
01	only row

'''


# * Mock load_table('table-name')
# * Capture sys.stdout and compare
def test_print_plain_tables_table(capsys, monkeypatch, one_item_table,
                                  two_item_table, tables_table):
    def mock_load_table(table_name):
        if table_name == 'one-item-table':
            return one_item_table
        elif table_name == 'two-item-table':
            return two_item_table
        elif table_name == 'tables-table':
            return tables_table

    monkeypatch.setattr(tablator.table, "load_table", mock_load_table)
    tablator.table.print_plain('tables-table')
    out, err = capsys.readouterr()
    #with capsys.disabled():
    #    print('out', out, sep='\n')
    assert out == '''\
 d50	Tables Table
-----	------------
01-25	One Item Table
26-50	Two Item Table

'''


# * Mock load_table('table-name')
# * Capture sys.stdout and compare
def test_print_plain_table_list(capsys, monkeypatch, table_list):

    def mock_get_table_name(table_name):
        if table_name == 'two-item-table':
            return 'Two Item Table'
        else:
            return 'Unknown'

    def mock_load_table(table_name):
        return table_list

    monkeypatch.setattr(tablator.table, "get_table_name", mock_get_table_name)
    monkeypatch.setattr(tablator.table, "load_table", mock_load_table)
    tablator.table.print_plain('table-list')
    out, err = capsys.readouterr()
    #with capsys.disabled():
    #    print('out', out, sep='\n')
    assert out == '''\
Table List
----------
 50% 1 First Table
 80% 1 Second Table
 35% 2 Two Item Table

'''


def test_random_row_1(one_item_table):
    # Get a "random" row from a one-row table.
    row = tablator.table.random_row(one_item_table)
    assert isinstance(row, dict)
    assert row['weight'] == 1
    assert row['name'] == 'only row'


def test_random_row_2(two_item_table):
    # Get a "random" row from a two-row table.
    row = tablator.table.random_row(two_item_table)
    assert isinstance(row, dict)
    assert row['weight'] == 1
    assert row['name'] == 'row one' or row['name'] == 'row two'


def test_roll_quantity_1():
    n = tablator.table.roll_quantity('1')
    assert n == '1'


def test_roll_quantity_2():
    n = tablator.table.roll_quantity('12')
    assert n == '12'


def test_roll_quantity_3():
    for i in range(100):
        n = tablator.table.roll_quantity('1d6')
        assert int(n) >= 1 and int(n) <= 6


def test_roll_quantity_4():
    for i in range(100):
        n = tablator.table.roll_quantity('3d9')
        assert int(n) >= 3 and int(n) <= 27


def test_roll_quantity_5():
    for i in range(100):
        n = tablator.table.roll_quantity('1d6+10')
        assert int(n) >= 10 and int(n) <= 16


def test_roll_quantity_6():
    for i in range(100):
        n = tablator.table.roll_quantity('10d6-10')
        assert int(n) >= 0 and int(n) <= 50


def test_roll_quantity_7():
    for i in range(100):
        n = tablator.table.roll_quantity('10d10+10x100')
        assert int(n) >= 2000 and int(n) <= 11000

