#!/bin/bash
# Test script to verify all tables in DATA_DIR are correct.
# List all tables files in this directory.
# Then, print each table.
if [ "$1" == "-h" ] || [ "$1" == "--help" ]; then
    readonly N="$(basename "$0")"
    cat <<EOD

    $N DATA_DIR - list and print tables  

EOD
    exit 0
fi

set -e      # fail if any command fails

readonly BASE_DIR="$(cd $(dirname "$0")/.. && echo $PWD)"
readonly DATA_DIR="${1:-$BASE_DIR/data}"
if [ ! -d "$DATA_DIR" ]; then
    echo "Data directory does not exist: $DATA_DIR"
    exit 1
fi

readonly PYTHON="$(command -v python3)"
readonly TABLATOR="$BASE_DIR/src/tablator.py"
export PYTHONPATH="$BASE_DIR/src"

# List tables
"$PYTHON" "$TABLATOR" --data-dir "$DATA_DIR" --list

# Print all tables
for json_file in $(find "$DATA_DIR" -name \*.json | sort); do
    table="$(basename "$json_file" .json)"
    printf '%s\n' ">>> Table: $table"
    "$PYTHON" "$TABLATOR" --data-dir "$DATA_DIR" --print "$table"
    [ $? -eq 0 ] || { echo ">>> Printing '$table' returned: $?"; exit 1; }
done
for yaml_file in $(find "$DATA_DIR" -name \*.yaml| sort); do
    table="$(basename "$yaml_file" .yaml)"
    printf '%s\n' ">>> Table: $table"
    "$PYTHON" "$TABLATOR" --data-dir "$DATA_DIR" --print "$table"
    [ $? -eq 0 ] || { echo ">>> Printing '$table' returned: $?"; exit 1; }
done
