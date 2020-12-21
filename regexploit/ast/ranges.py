from dataclasses import dataclass
from typing import Iterator, List, Set, Tuple


@dataclass(frozen=True)
class Range:
    min_val: int
    max_val: int


def lits_to_ranges(
    literals: Iterator[int],
) -> Tuple[Set[int], Set[Range]]:
    lits = set()
    ranges = set()
    buf: List[int] = []
    for lit in sorted(literals):
        if len(buf) and buf[-1] != lit - 1:
            # Discontinuity
            if len(buf) < 3:
                lits.update(buf)
            else:
                ranges.add(Range(buf[0], buf[-1]))
            buf = [lit]
        else:
            buf.append(lit)

    if len(buf) == 1:
        lits.add(buf[0])
    elif len(buf) > 1:
        ranges.add(Range(buf[0], buf[-1]))

    return lits, ranges
