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
to write another script, unless something more specialized is desired.

```
python3 tablator.py --help
python3 tablator.py rings wands weapons
python3 tablator.py lair-a
python3 tablator.py --number 3 potions
python3 tablator.py --print scrolls
python3 tablator.py --data-dir ~/data/pathfinder-encounters dungeon-mid
python3 tablator.py -c addt.conf magic-item -n 3
```

1. Print usage information.
2. Roll once on each of the _rings_, _wands_, and _weapons_ tables.
3. Roll on the "Lair A" table.
4. Roll three itmes on the "potions" table.
5. Print the scrolls table to the terminal.
6. Roll on the "Dungon Mid-level Dungeon Encounters" table in the specified data directory.
7. Roll four times on the magic items table using the given configuration file.

### Environment Variables

The data directory file is set from `TABLATOR_DATA_DIR` if it is found in the
environment.

The configuration file is set from `TABLATOR_CONFIG_FILE` if it is found in the
environment.

Settings on the command line override the values from the environment.

### Configuration file

The configuration file provides a set of default values for the same options
that are set by the command line arguments. The following files are used,
in this order, to set configuration defaults.

- `~/.ttrc` -- In the user's home directory
- `./.ttrc` -- In the current directory
- `--config FILE` -- Anywhere in the host's file system

This is an example configuration file.

```
# Pathfinder Core
data-dir = ~/Public/tablator-data/pathfinder-core
trace = no
verbose = yes
```

Tilde expansion is performed on _data-dir_, but environment variables are not.

Settings on the command line or in the environment override the values in the
configuration file.

### The Data Directory

The _Data Directory_ is a file system directory where a set of related
_tablator_ table files are found.
Table files are JSON or YAML formatted files found in this directory.
For example, if the command `python3 tablator.py potions` is entered,
then there must be a correctly formatted file called "potions.json" or
"potions.yaml" in DATA_DIR. Similarly, if a table row has a subtable or table
key, then there must be a corresponding table file in DATA_DIR.

In the `tablator` tool, the data diretory is set as a command line argument,
from the environment variable `TABLATOR_DATA_DIR`, or in the configuration file.
If not set, it defaults to the current working directory.

In Python the data directory is set thusly:

```python
tablator.data.set_data_dir('~/data')
```

## Table DATA Format

The library is designed to load tables in JSON and YAML format.  The reference
tables were all done in JSON so that's the format of the examples.

There are two kinds of tables: the _row_ table and the _column_ table.

### Row Table

A _row table_ is a single look-up table from which one row is selected at
random.  Its attributes are:

* __name__ is required, a string
* __total-weight__ is required, a number
* __rows__ is required, an array
* __rows[i].name__ is required, a string
* __rows[i].weight__ is optional, a number, defaults to 1
* __rows[i].table__ is optional, a string naming a table
* __rows[i].subtable__ is optional, a string naming a table
* __rows[i].quantity__ is optional, a dice expression, defaults to 1
* __rows[i].units__ is optional, a string, appended to quantity result

The top-level __name__ is the table's name or title.

The __total-weight__ is the sum of the row's weights.

The __rows__ is an array of item entries.  Each row entry requires a __name__
or __table__ and a __weight__.  If __table__ is present, it is the name of a
from which an item is rolled in place of the __name__ of this item's name.
If not present, __weight__ is 1.
If __quantity__ is present, the _dice expression_ is rolled to generate the
item count which is included as an item attribute.
If __units__ is present and quantity is greater than one, it is appended to the
quantity attribute.
If __subtable__ is present, then an item is randomly selected from that
table.  The name fo the item from the subtable is included as an attribute in
parentheses after the primary table item.

If __table__ is present, it replaces the entire item with a result from a
lookup in another table.  No other row attributes are processed.  This kind of
_Items Table_ requires only __rows[i].table__ and __rows[i].weight__ keys.

For example, the following table

```json
{
  "name": "Office Supplies",
  "total-weight": 100,
  "rows": [
    {
      "weight": 25,
      "name": "notebook"
    },
    {
      "weight": 50,
      "name": "ink pens",
      "subtable": "colors",
      "quantity": "2d6",
    },
    {
      "weight": 25,
      "name": "printer paper",
      "quantity": "2d10",
      "units": "reams",
    }
  ]
}
```

can produce output like

```text
notebook
ink pens (9, blue)
printer paper (8 reams)
```

A row table can be a table of tables where each item is a lookup from another
table.

```json
{
  "name": "Table of Tables",
  "total-weight": 3,
  "rows": [
    { "table": "fruits" },
    { "table": "vegetables" },
    { "table": "grains" }
  ]
}
```

Note also that weights are relative.
The above example could have _total-weight_ of 10 and row _weight_ of 3, 4,
and 3 for a d10-based table, or 4, 4, 4 for a d12-based table.

### Column Table

A list of tables. Roll once on every table (column) in the list.

* __name__ required, a string
* __columns__ is required, an array
* __columns[i].chance__ is optional, a number in 1-100, chance of item occurring
    on d%, defaults to 100
* __columns[i].name__ is required, a string, item name (used if table is null)
* __columns[i].quantity__ is optional, a dice expression, number of rolls on
    table or number of items, defaults to 1
* __columns[i].table__ = is optional, a string, roll on this table 'quantity'
    times, defaults to _null_

The top-level __name__ is the table's name or title.

Each column has a percent __chance__ to occur.  If a d100 roll is less than
__chance__, the item is present. If the roll fails, the column is skipped.

One of  __name__ or __table__ is required in each column entry.
If __table__ is present, then __quantity__ rolls are be made on that table.
 Otherwise, it rolls __quantity__ of __name__.

```json
{
  "name": "Table List Name",
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
   },
   {
      "chance" : 20,
      "name": "Thing D"
   }
 ]
}
```

In the above example, there is an 80% chance of generating 2-8 items from
"table-a", a 15% chance of generating one item from "table-b", a 50% chance
of generating 100-1000 of "Thing C", and a 20% chance for one "Thing D".

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

Dependencies for development

```
apt install python3-pytest python3-pytest-cov
sudo python3 -m pip install pytest pytest-cov       # An alternative
```

## The man page

```
man -l tablator.1
```

## Tests

Install `python3-pytest`.

Optionally install `python-pytest-doc`, `python3-pytest`,
`python3-pytest-cov`, `python3-pytest-flake8`, `python3-pytest-mock`,
`python3-pytest-pep`, `python3-pytest-pylint`, `python3-pytest-runner`.

Run the tests with coverage report from the root of the repository.

```shell
tests/run.sh
```
