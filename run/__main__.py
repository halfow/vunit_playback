"""
This script runs when module is called via 'python -m <FOLDERNAME>'.
"""
from vunit import VUnit
from pathlib import Path
from . import prompt, create, add

vunit = VUnit.from_argv()
vunit.add_array_util()

# Structural
todo = [
    add.files,
    add.configs,
    create.vhdl_ls_config,
    create.hdl_checker_config,
    prompt.multiple_tests_with_gui,
]

[f(vunit) for f in todo]

vunit.main()
