# Tablator

Randomly select items from lookup tables.

The _tablator_ library is a general purpose library for randomly generating
results from look-up tables.

Tab-LA-tor.  Originally called "treasure tables" was developed to roll up magic
items from the treasure tables in the AD&D DMG.  It has nothing to do with
guitar tablature.

## The Tablator Tool

The _tablator.py_ script is a reference implementation to show how the
_tablator_ library is used.  It can be used to roll on tables without the need
to write another script, unless something more specialized is necessary.

```
python3 tablator.py --help
python3 tablator.py lair-a
python3 tablator.py --number 3 potions
python3 tablator.py --print scrolls
python3 tablator.py --data-dir ~/data/pathfinder-encounters dungeon-mid
python3 tablator.py --config addt.conf magic-item --number 3
```

### Configuration file

The configuration file provides a set of default values for the same options
that are set by the command line arguments.  Setting on the command file
override the values in the configuration file.  The following files are used,
in this order, to set configuration defaults.

- `~/..ttrc`
- `./.ttrc`
- --config _FILE_

This is an example configuration file.

```
# Pathfinder Core
data-dir = ~/Source/tablator-data/pathfinder-core
trace = no
verbose = yes
```

Tilde expansion is performed on _data-dir_, but environment variables are not.

## Table DATA Format

The library is designed to load tables in JSON and YAML format.  The reference
tables were all done in JSON so that's the format of the examples.

There are three kinds of tables: the _items_ table, the _tables_ table, and the
_table_list_ table. Each is described in more detail below.

### The DATA_DIR

Every table is a JSON or YAML formatted file found in the data directory.
For example, if the command `python3 treasure-table.py potions` is entered,
then there must be a correctly formatted file called "potions.json" or
"potions.yaml" in DATA_DIR. Similarly, if a table row has a subtable key,
then there must be a corresponding table file in DATA_DIR.

(how to set the DATA_DIR)
```python
tablator.data.set_data_dir('/tmp/data')
```

### Items Table

Items table randomly select an item from the table.  If there is an optional
subtable, then an item is randomly selected from that table.  The name of the
item in the subtable is included in parentheses after the primary table item.

The items table has the following fields.

* __name__ is required, a string
* __type__ is required, the string "items"
* __total-weight__ is required, a number
* __rows__ is required, an array
* __rows[i].name__ is required, a string
* __rows[i].weight__ is optional, a number, defaults to 1
* __rows[i].subtable__ is optional, a string naming a table
* __rows[i].quantity__ is optional, a dice expression, defaults to 1
* __rows[i].value__ is optional, a dice-expression, defaults to 1

If __quantity__ is present, __value__ is ignored. Item __value__ is a special
case hack added to accomadate gem and jewelry tables.
The unit of __value__ is "gold pieces" (gp).

If __subtable__ is present, it is included in the current item.  Subtables are
for adding attributes to the item.

If __table__ is present, it replaces the entire item with a result from a
lookup in another table.  No other row attributes are processed.

```json
{
  "name": "Headwear",
  "type": "items",
  "total-weight": 100,
  "rows": [
    {
      "name": "Hat",
      "weight": 75,
      "quantity": "2d6",
      "subtable": "colors"
    },
    {
      "name": "Helmet",
      "weight": 25,
      "subtable": "colors"
    }
  ]
}
```

This example is a table of items named "Headwear" where there is a 75%
chance (75 of 100) to select "Hat" and a 25% chance to select "Helmet".
Both selections will have an attribute from the "colors" subtable.
If "Hat" is selected, it will have a quantity of 2-12.

The tables are in the `data` directory. The "colors" and "hats" tables are
minimal item list tables where items have only a __name__  and a default
__weight__ of 1.


```text
$ src/tablator.py -d data headwear -n 4
hats (red, 6)
hats (green, 2)
helmet (blue)
hats (green, 11)
```

### Tables Table

The tables table randomly selects a subtable.  A random item is then selected
from the subtable.

The tables table has these fields.

* __name__ is required, a string
* __type__ is required, the string "tables"
* __total-weight__ is required, a number
* __rows__ is required, an array
* __rows[i].weight__ is optional, a number, defaults to 1
* __rows[i].table__ is required, a string naming a table

```json
{
  "name": "Transportation",
  "type": "tables",
  "total-weight": 100,
  "rows": [
    {
      "table": "automobiles"
      "weight": 40,
    },
    {
      "table": "busses"
      "weight": 40,
    },
    {
      "table": "aircraft"
      "weight": 20,
    }
  ]
}
```

This example is of a table named ``Transportation'' which has a 40% chance (40
of 100) to generate an item from the ``automobiles'' subtable, a 40% chance to
generate an item from the ``busses`` subtable, and a 20% chance to generate an
item from the ``aircraft'' subtable.

### Table List Table

A list of tables. Roll once on every table (column) in the list.

This table has two modes of operation.  If _table_ is _null_, it may generate
_quantity_ of _name_.  If _table_ is not _null_, then _quantity_ rolls may be
made on the _table_.

For each _column_, it is generated if d% is less than or equal to _chance_ for
that column.  If the roll fails, the column is skipped.

The table list table has the following fields.

* __name__ required, a string
* __type__ is required, the string "table-list"
* __columns__ is required, an array
* __columns[i].chance__ is optional, a number in 1-100, chance of item occurring
    on d%, defaults to 100
* __columns[i].name__ is required, a string, item name (used if table is null)
* __columns[i].quantity__ is optional, a dice expression, number of rolls on
    table or number of items, defaults to 1
* __columns[i].table__ = is required, a string, roll on this table 'quantity'
    times or _null_

```json
{
  "name": "Table List Name",
  "type": "table-list",
  "columns" : [
    {
      "chance" : 80,
      "name": "Thing A",
      "quantity": "2d4",
      "table" : "table-a"
   },
   {
      "chance" : 15,
      "name": "Thing B",
      "quantity": "1",
      "table" : "table-b"
   },
   {
      "chance" : 50,
      "name": "Thing C",
      "quantity": "1d10x100",
      "table" : null
   }
 ]
}
```

In the above example, there is an 80% chance of generating 2-8 items from
"table-a", a 15% chance of generating one item from "table-b", and a 50% chance
of generating 100-1000 of "Thing C".

### Dice Expression

A _dice expression_ is a short-hand way to define a set of dice to roll with
adds or multipliers.
Input is a string, output is a number (integer).
Here are some examples to illustrate.

```
10 -> 10
1d8 -> 1-8
3d6 -> 1-6 + 1-6 + 1-6
1d4-1 -> 1-4 - 1
2d6+6 -> 1-6 + 1-6 + 6
10d10x10 -> (1-10 + ... + 1-10) x 10
2d4+2x10 -> (1-4 + 1-4 + 2) x 10
```

## Clone & Install

```
git clone https://github.com/crithead/tablator
cd tablator
sudo python3 -m pip install --upgrade pip               # optional
sudo python3 -m pip install --upgrade setuptools        # optional
python3 setup.py --install --user
python3 -c 'import tablator'                            # verify
```

## Build the man page

```
pandoc --standalone -t man -o build/tablator.1 tablator.1.md
man -l build/tablator.1
```
