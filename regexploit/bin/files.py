import os
import os.path
from glob import iglob
from typing import List, Optional


def _file_generator(
    files_argument: List[str], is_glob: bool, filename_globs: List[str]
):
    if is_glob:
        for fglob in files_argument:
            yield from iglob(fglob, recursive=True)
    else:
        for f in files_argument:
            if os.path.isdir(f):
                for g in filename_globs:
                    yield from iglob(os.path.join(f, "**", g), recursive=True)
            else:
                yield f


def file_generator(
    files_argument: List[str],
    is_glob: bool,
    filename_globs: List[str],
    ignore: Optional[List[str]] = None,
):
    gen = _file_generator(files_argument, is_glob, filename_globs)
    if ignore:
        for f in gen:
            if any(i in f for i in ignore):
                continue
            yield f
    else:
        yield from gen
