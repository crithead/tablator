#!/bin/bash
readonly SCR_DIR="$(dirname "$(realpath "$0")")"
readonly SRC="$(realpath "${SCR_DIR}/../src")"
PYTHONPATH="${SRC}" pytest -v --capture=sys --cov=tablator
