#!/bin/bash

current_dir=$(dirname "$0")

venv_path="$current_dir/.pyenv"

source "$venv_path/bin/activate"

main_py_path="$current_dir/main.py"

# Pass the arguments to the main.py file
python "$main_py_path" "$@"

# Turn off the virtual environment
deactivate
