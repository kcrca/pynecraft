from typing import Tuple

from pynecraft.commands import Commands, DataTarget, SUCCESS, Score, data, execute, scoreboard
from pynecraft.values import DUMMY

PYNECRAFT = 'pynecraft'


def utils_init() -> Commands:
    return scoreboard().objectives().add(PYNECRAFT, DUMMY)


class Scores:
    strcmp = Score('strcmp_differ', PYNECRAFT)


def strcmp(v1: str | Tuple[DataTarget, str], v2: str | Tuple[DataTarget, str]) -> Commands:
    """
    Returns commands that compares two strings. The strings are either literals or data targets for the strings. The
    result is stored in the score ``compare_strings_differ`` in the ``pynecraft`` objective, which is 1 if they
    differ or 0 if they are the same. (Data targets are tuples that have the data source and the NBT path inside that
    source.)
    """
    setter = data().modify(PYNECRAFT, 'strcmp.value').set()

    def complete(v) -> str:
        if isinstance(v, str):
            return setter.value(v)
        else:
            return setter.from_(*v)

    c1 = complete(v1)
    r1 = complete(v2)
    c2 = execute().store(SUCCESS).score(Scores.strcmp).run(r1)
    return c1, c2
