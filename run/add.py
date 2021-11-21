"""
Add files, config, parameters etc.
**********************************

TODO: a wrapper function should probably be used to make 
      it easy to import for stuff like "deep" regression.

.. code-block:: python
"""
from vunit import VUnit
from pathlib import Path


def files(vunit: VUnit) -> None:
    """
    **Source and test files**

    Args:
    .. code-block:: text
        vunit (VUnit): Vunit Project
    
    *Example:*
    .. code-block:: python
        vunit.library(lib).add_file(path)
        or 
        vunit.library(lib).add_files(paths or globs)
    """
    root = Path(__file__).parent.parent
    lib = vunit.add_library(root.name)
    lib.add_source_files(root / "*/*.vhd")


def configs(vunit: VUnit) -> None:
    """
    **Configure additional tests** 

    Args:
    .. code-block:: text
        vunit (VUnit): Vunit Project
    
    **Example:**
    
    ------------------------------------
    *python:*
    .. code-block:: python
        vunit.set_generic("csv", path)  # <- Not recommended
        or
        vunit.library(lib).test_bench(tb).add_config(
            name, generics=dict(csv=path))
        or
        vunit.library(lib).test_bench(tb).test(test).add_config(
            name, generics=dict(csv=path))
    ------------------------------------
    *vhdl:*
    .. code-block:: vhdl
        entity *_tb is
            generic (
                csv : string;
                runner_cfg : string
                );
        end entity;
    ------------------------------------
    """
    root = Path(__file__).parent.parent
    for tb in vunit.library(root.name).get_test_benches():
        for stimuli in root.glob("test/stimuli/*"):
            tb.add_config(
                name=stimuli.stem,
                generics=dict(csv=str(stimuli))
            )
