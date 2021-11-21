"""
Create Config files for linters and formatters
**********************************************
*Example:*
.. code-block:: python
    from . import create
    create.hdl_checker_config(vunit)
    create.vhdl_ls_config(vunit)
"""
from vunit import VUnit
from collections import defaultdict
from typing import Dict
from pathlib import Path
import json


def hdl_checker_config(vunit: VUnit) -> None:
    """
    **Create hdl_checker config file**

    Args:
    .. code-block:: text
        vunit (VUnit): Vunit project

    TODO: add simulator to be used, Get from vunit or explicit setting?   

    *Example:*
    .. code-block:: json
        {
            "sources": [
                ["path1", {"library": "lib", "flags": ["-2008"]}],
                ["path2", {"library": "lib", "flags": ["-93"]}]
            ]
        }
    """
    config: Dict[str, list] = dict(sources=[])
    for source_file in vunit.get_compile_order():
        config["sources"].append([
            str(Path(source_file.name).resolve()),
            dict(
                # TODO: should the path be absolute to avoid errors?
                library=source_file.library.name,
                flags=[f"-{source_file.vhdl_standard}"]
            )
        ])
    # NOTE: only linux support for now
    # TODO: get os so . _ as starting char can be resolved
    with open(".hdl_checker.config", "w+") as fp:
        json.dump(config, fp, indent=4)


def vhdl_ls_config(vunit: VUnit) -> None:
    """
    **Create a vhdl_ls config file**

    Args:
    .. code-block:: text
        vunit (VUnit): Vunit project

    *Example:*
    .. code-block:: toml
        [library]
        lib.files = [
            "path1",
            "path2"
        ]
    """
    fileslist = defaultdict(list)
    for source_file in vunit.get_compile_order():
        # TODO: should the path be absolute to avoid errors?
        fileslist[source_file.library.name].append(
            str(Path(source_file.name).resolve()))

    # TODO: Raymond Hettinger knows whats up... there must be a better way!
    with open("vhdl_ls.toml", "w+") as fp:
        fp.write("[library]\n")
        for lib, files in fileslist.items():
            fp.write(f"{lib}.files = [\n\t")
            fp.write("\n\t".join(map('"{}"'.format, files)))
            fp.write("\n]\n")
