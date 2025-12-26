# PyTest for tablator.table

import pytest
import tablator.table
import tablator.logger

@pytest.fixture
def one_row_table():
     return {
        'name': 'One Row Table',
        'total-weight': 1,
        'rows': [
            {
                'weight': 1,
                'name': 'only row'
            }
        ]
    }

@pytest.fixture
def two_row_table():
     return {
        'name': 'Two Row Table',
        'total-weight': 2,
        'rows': [
            { 'weight': 1, 'name': 'row one' },
            { 'weight': 1, 'name': 'row two' }
        ]
    }

@pytest.fixture
def default_weight_table():
     return {
        'name': 'Two Row Table',
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
def nine_row_table():
     return {
        'name': 'Nine Row Table',
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
        'total-weight': 1,
        'rows': [
            {
                'weight': 1,
                'name': 'only subtable row',
                'subtable': 'one-row-table'
            }
        ]
    }


@pytest.fixture
def one_subtable_quantity_table():
     return {
        'name': 'One Subtable Table with Quantity',
        'total-weight': 10,
        'rows': [
            {
                'weight': 10,
                'name': 'only subtable row',
                'subtable': 'one-row-table',
                'quantity': '20'
            }
        ]
    }


@pytest.fixture
def one_subtable_quantity_units_table():
     return {
        'name': 'One Subtable Table with Value',
        'total-weight': 10,
        'rows': [
            {
                'weight': 10,
                'name': 'only subtable row',
                'subtable': 'one-row-table',
                'quantity': '1000',
                'units': 'widgets'
            }
        ]
    }


@pytest.fixture
def bad_weight_table():
     return {
        'name': 'Bad Weight Row Table',
        'total-weight': 10,
        'rows': [
            { 'weight': 2, 'name': 'row one' },
            { 'weight': 4, 'name': 'row two' },
            { 'weight': 8, 'name': 'row three' },
            { 'weight': 4, 'name': 'row four' },
            { 'weight': 2, 'name': 'row five' }
        ]
    }


@pytest.fixture
def columns_table():
     return {
        'name': 'Table List',
        'total-weight': 3,
        'columns': [
            {
                'chance': 50,
                'name': 'First Item',
                'quantity': '1',
            },
            {
                'chance': 80,
                'name': 'Second Item',
                'quantity': '1',
            },
            {
                'chance': 35,
                'table': 'two-row-table',
                'quantity': '2',
            },
        ]
    }


@pytest.fixture
def columns_table_no_chance():
     return {
        'name': 'Table List, No Chance',
        'total-weight': 2,
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
def columns_table_bad_chance():
     return {
        'name': 'Table List, Bad Chance',
        'total-weight': 2,
        'columns': [
            {
                'name': 'First Table',
                'chance': -99,
                'table': 'one-row-table'
            },
            {
                'name': 'Second Table',
                'chance': 1234,
                'table': 'one-row-table'
            },
        ]
    }


def test_check_weights_1(one_row_table):
    try:
        tablator.table.check_weights(one_row_table)
    except ValueError as e:
        assert False, f'unexpected exception: {e}'


def test_check_weights_2(nine_row_table):
    try:
        tablator.table.check_weights(nine_row_table)
    except ValueError as e:
        assert False, f'unexpected exception: {e}'


def test_check_weights_default_weights(default_weight_table):
    try:
        tablator.table.check_weights(default_weight_table)
    except ValueError as e:
        assert False, f'unexpected exception: {e}'


def test_check_weights_columns(capsys, columns_table):
    try:
        tablator.table.check_weights(columns_table)
    except ValueError as e:
        assert False


def test_check_weights_bad_weights(bad_weight_table):
    with pytest.raises(ValueError, match=r".* row weights don't add up: .*"):
        tablator.table.check_weights(bad_weight_table)


def test_generate_invalid_table(monkeypatch):
    def mock_load_table(table_name):
        return None

    with pytest.raises(ValueError, match='Table not found: no-table'):
        tablator.table.generate('no-table', 1)


def test_generate_row_table(monkeypatch, one_row_table):
    def mock_load_table(table_name):
        return one_row_table

    monkeypatch.setattr(tablator.table, 'load_table', mock_load_table)
    values = tablator.table.generate('one-row-table', 3)
    assert values == ['only row', 'only row', 'only row']


def test_generate_columns_table(monkeypatch, one_row_table):
    def mock_load_table(table_name):
        return one_row_table

    def mock_lookup_columns(table_name):
        return ['only row']

    monkeypatch.setattr(tablator.table, 'load_table', mock_load_table)
    monkeypatch.setattr(tablator.table, 'lookup_columns', mock_lookup_columns)
    values = tablator.table.generate('list-table', 3)
    assert values == ['only row', 'only row', 'only row']


def test_get_chance_not_present(columns_table_no_chance):
    chance = tablator.table.get_chance(columns_table_no_chance['columns'][0])
    assert chance == 100
    chance = tablator.table.get_chance(columns_table_no_chance['columns'][1])
    assert chance == 100


def test_get_chance_invalid_chance(columns_table_bad_chance):
    with pytest.raises(ValueError, match='Column chance out of range: -99'):
        chance = tablator.table.get_chance(columns_table_bad_chance['columns'][0])
    with pytest.raises(ValueError, match='Column chance out of range: 1234'):
        chance = tablator.table.get_chance(columns_table_bad_chance['columns'][1])


def test_get_chance_ok(columns_table):
    chance = tablator.table.get_chance(columns_table['columns'][0])
    assert chance == 50
    chance = tablator.table.get_chance(columns_table['columns'][1])
    assert chance == 80
    chance = tablator.table.get_chance(columns_table['columns'][2])
    assert chance == 35


def test_get_table_name_ok(monkeypatch, one_row_table):
    def mock_load_table(table_name):
        return one_row_table

    monkeypatch.setattr(tablator.table, 'load_table', mock_load_table)
    name = tablator.table.get_table_name('one-row-table')
    assert name == 'One Row Table'
    assert name == one_row_table['name']


def test_get_table_name_no_name(monkeypatch):
    def mock_load_table(table_name):
        return dict()

    monkeypatch.setattr(tablator.table, 'load_table', mock_load_table)
    with pytest.raises(KeyError):
        chance = tablator.table.get_table_name('empty-table')


def test_load_table_cache_miss(capsys, monkeypatch, one_row_table):
    def mock_load(table_name):
        return one_row_table

    tablator.table._tables.clear()      # clear the table cache
    tablator.logger.set(True, False)    # enable debug output
    monkeypatch.setattr(tablator.data, 'load', mock_load)
    table = tablator.table.load_table('one-row-table')
    tablator.logger.set(False, False)   # disable debug output
    out, err = capsys.readouterr()
    assert '--- loaded one-row-table' in out
    assert table is not None


def test_load_table_cache_hit(capsys, monkeypatch, one_row_table):
    def mock_load(table_name):
        return one_row_table

    tablator.table._tables.clear()      # clear the table cache
    tablator.logger.set(False, False)   # disable debug output
    monkeypatch.setattr(tablator.data, 'load', mock_load)
    # Call once to load the table cache
    table = tablator.table.load_table('one-row-table')
    tablator.logger.set(True, False)    # enable debug output
    # Now get table from the table cache
    table = tablator.table.load_table('one-row-table')
    tablator.logger.set(False, False)   # disable debug output
    out, err = capsys.readouterr()
    assert '--- cache hit one-row-table' in out
    assert table is not None


def test_lookup_rows_simple_lookup(monkeypatch, one_row_table):
    def mock_random_row(table_name):
        return { 'name': 'fake row' }

    monkeypatch.setattr(tablator.table, 'random_row', mock_random_row)
    row_name = tablator.table.lookup_rows(one_row_table)
    assert row_name == 'fake row'


def test_lookup_rows_quantity(monkeypatch, one_row_table):
    def mock_random_row(table_name):
        return { 'name': 'fake row', 'quantity': '10' }

    monkeypatch.setattr(tablator.table, 'random_row', mock_random_row)
    row_name = tablator.table.lookup_rows(one_row_table)
    assert row_name == 'fake row (10)'


def test_lookup_rows_subtable(monkeypatch, one_subtable_table, one_row_table):
    def mock_random_row(table):
        if table is one_subtable_table:
            return one_subtable_table['rows'][0]
        if table is one_row_table:
            return one_row_table['rows'][0]
        assert False, 'Invalid table!'

    def mock_load_table(table_name):
        return one_row_table

    monkeypatch.setattr(tablator.table, 'random_row', mock_random_row)
    monkeypatch.setattr(tablator.table, 'load_table', mock_load_table)
    row_name = tablator.table.lookup_rows(one_subtable_table)
    assert row_name == 'only subtable row (only row)'


def test_lookup_rows_subtable_quantity(monkeypatch, one_row_table,
                                        one_subtable_quantity_table):
    def mock_random_row(table):
        if table is one_subtable_quantity_table:
            return one_subtable_quantity_table['rows'][0]
        if table is one_row_table:
            return one_row_table['rows'][0]
        assert False, 'Invalid table!'

    def mock_load_table(table_name):
        return one_row_table

    monkeypatch.setattr(tablator.table, 'random_row', mock_random_row)
    monkeypatch.setattr(tablator.table, 'load_table', mock_load_table)
    row_name = tablator.table.lookup_rows(one_subtable_quantity_table)
    assert row_name == 'only subtable row (only row, 20)'


def test_lookup_rows_subtable_quantity_units(monkeypatch, one_row_table,
                                     one_subtable_quantity_units_table):
    def mock_random_row(table):
        if table is one_subtable_quantity_units_table:
            return one_subtable_quantity_units_table['rows'][0]
        if table is one_row_table:
            return one_row_table['rows'][0]
        assert False, 'Invalid table!'

    def mock_load_table(table_name):
        return one_row_table

    monkeypatch.setattr(tablator.table, 'random_row', mock_random_row)
    monkeypatch.setattr(tablator.table, 'load_table', mock_load_table)
    row_name = tablator.table.lookup_rows(one_subtable_quantity_units_table)
    assert row_name == 'only subtable row (only row, 1000 widgets)'


def test_lookup_columns_table():
    #tablator.table.lookup_columns(table)
    assert True


def test_lookup_columns():
    #tablator.table.lookup_columns(table)
    assert True


# * Mock load_table('table-name')
# * Capture sys.stdout and compare
def test_print_plain_row_table(capsys, monkeypatch, one_row_table):
    def mock_load_table(table_name):
        return one_row_table

    monkeypatch.setattr(tablator.table, "load_table", mock_load_table)
    tablator.table.print_plain('one-row-table')
    out, err = capsys.readouterr()
    with capsys.disabled():
        print('out', out, sep='\n')
    assert out == '''\
 d1	One Row Table
-----	-------------
01	only row

'''


# * Mock load_table('table-name')
# * Capture sys.stdout and compare
def test_print_plain_columns_table(capsys, monkeypatch, columns_table):

    def mock_get_table_name(table_name):
        if table_name == 'two-row-table':
            return 'Two Row Table'
        else:
            return 'Unknown'

    def mock_load_table(table_name):
        return columns_table

    monkeypatch.setattr(tablator.table, "get_table_name", mock_get_table_name)
    monkeypatch.setattr(tablator.table, "load_table", mock_load_table)
    tablator.table.print_plain('tables')
    out, err = capsys.readouterr()
    #with capsys.disabled():
    #    print('out', out, sep='\n')
    assert out == '''\
Table List
----------
 50% First Item
 80% Second Item
 35% 2 Two Row Table

'''


def test_random_row_1(one_row_table):
    # Get a "random" row from a one-row table.
    row = tablator.table.random_row(one_row_table)
    assert isinstance(row, dict)
    assert row['weight'] == 1
    assert row['name'] == 'only row'


def test_random_row_2(two_row_table):
    # Get a "random" row from a two-row table.
    row = tablator.table.random_row(two_row_table)
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
