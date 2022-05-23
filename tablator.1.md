---
title: tablator
section: 1
header: User Manual
footer: tablator 1.0.1
data: May 25, 2022
---

# NAME

**tablator** - prints a random item from a table

# SYNOPSIS

| **tablator** \[-c CONFIG] \[-d DATA_DIR] \[-l] \[-n NUMBER] \[-p] \[-t] \[-v] \[tables ...]
| **tablator** \[-c CONFIG] \[-d DATA_DIR] \[-l | --list]
| **tablator** \[-c CONFIG] \[-d DATA_DIR] \[-p | --print] table
| **tablator** \[ -h | --help ]

# DESCRIPTION

Randomly select items from lookup tables.

The tablator library is a general purpose library for randomly generating
results from look-up tables.

Tab-LA-tor. Originally called "treasure tables" was developed to roll up
magic items from the treasure tables in the AD&D DMG.
It has nothing to do with guitar tablature.


# OPTIONS

-h, --help
: show this help message and exit

-c *CONFIG*, --config *CONFIG*
: load configuration from this file

-d *DATA_DIR*, --data-dir *DATA_DIR*
: set the table data directory

-l, --list
: list available tables

-n *NUMBER*, --number *NUMBER*
: number of items to select from each table (default 1)

-p, --print
: print the table (plain text)

-t, --trace
: enable trace messages

-v, --verbose
: enable debug messages

# EXAMPLES

    python3 tablator.py --help
    python3 tablator.py lair-a
    python3 tablator.py --number 3 potions
    python3 tablator.py --print scrolls
    python3 tablator.py --data-dir ~/data/pathfinder-encounters dungeon-mid
    python3 tablator.py --config addt.conf magic-item --number 3

# FILES

* -c *FILE*
* ./tablator.conf
* ~/.tablator

## CONFIGURATION

The configuration file is a list of long command line options and values.

# ENVIRONMENT

Maybe.

# BUGS

Maybe.

# SEE ALSO

The [README](https://github.com/crithead/tablator) along with the source.

