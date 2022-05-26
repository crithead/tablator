import pytest
import tablator.table

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
                'chance': 35,
                'name': 'Second Table',
                'quantity': '2',
                'table': 'two-item-table'
            },
        ]
    }


def test_check_weights():
    #tablator.table.check_weights(table)
    assert True


def test_generate():
    #tablator.table.generate(table_name, num_rolls=1)
    assert True


def test_get_chance():
    #tablator.table.get_chance(column)
    assert True


def test_get_table_name():
    #tablator.table.get_table_name(table_name)
    assert True


def test_load_table():
    #tablator.table.load_table(table_name)
    assert True


def test_lookup_items():
    #tablator.table.lookup_items(table)
    assert True


def test_lookup_table_list():
    #tablator.table.lookup_table_list(table)
    assert True


def test_lookup_tables():
    #tablator.table.lookup_tables(table)
    assert True


# * Mock load_table('table-name')
# * Capture sys.stdout and compare
# TODO Three versions of this test: items, tables, table-list
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

