"""
Prompt user for stuff...
"""
from vunit import VUnit
from rich.prompt import Confirm


def multiple_tests_with_gui(vunit: VUnit) -> None:
    """
    **Prompt if multiple test would run with gui flag**

    Args:
    .. code-block:: text
        vunit (VUnit): Vunit project

    Raises:
    .. code-block:: text
        SystemExit: Break if user input is no/false/n

    *Example:*
    .. code-block:: bash
        $ python -m run
        Test pattern '*' matches 2 tests, still want gui mode? [y/n]:
    """

    if vunit._args.gui and not any(
        # Arguments that not runs any test
        (vunit._args.files, vunit._args.list, vunit._args.compile)
    ):
        n = vunit._create_tests(simulator_if=None).num_tests
        if n > 1 and not Confirm.ask(
            f"Test pattern {vunit._args.test_patterns!r} matches {n} tests, still want gui mode?"
        ):
            raise SystemExit(1)
