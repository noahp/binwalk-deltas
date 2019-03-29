"""
Print deltas in binwalk output. Use like:
python binwalk-deltas.py <(binwalk BINFILE) BINFILE
"""
from __future__ import print_function
from errno import EPIPE
import re
import sys
import os
from functools import wraps

import humanize


def suppress_broken_pipe_msg(function):
    """Python when printing to a pager (less), if you exit without
    reading all the output, you get an ugly but harmless exception:
        BrokenPipeError: [Errno 32] Broken pipe
    If you try to just trap the error, you still get this print
    on python3:
        Exception ignored in: <_io.TextIOWrapper name='<stdout>' mode='w' encoding='UTF-8'>
        BrokenPipeError: [Errno 32] Broken pipe
    Found an answer on stackoverflow that gets us close.
    https://stackoverflow.com/a/35761190
"""

    @wraps(function)
    def wrapper(*args, **kwargs):
        """Wrap a function so we don't get ugly BrokenPipeErrors"""

        try:
            broken_pipe_exception = BrokenPipeError
        except NameError:  # Python 2
            broken_pipe_exception = IOError

        try:
            return function(*args, **kwargs)
        except SystemExit:
            raise
        except broken_pipe_exception as exc:
            if broken_pipe_exception == IOError:
                if exc.errno != EPIPE:
                    raise

    return wrapper


def print_entry(offset, size, name, human=False):
    """Print a binwalk entry"""
    if human:
        size = humanize.naturalsize(size)
    print("0x{:<10x} {:<15} {}".format(offset, size, name))


@suppress_broken_pipe_msg
def main():
    """Main cli entrance point"""
    binwalk_re = re.compile(r"(\d+)\s+0x[0-9a-fA-F]+\s+(.*)\s*$")

    entries = []

    filesize = os.stat(sys.argv[2]).st_size

    with open(sys.argv[1], "r") as infile:
        lastmatch = (None, None)
        for line in infile.readlines():
            match = binwalk_re.match(line.strip())
            if match:
                newmatch = (int(match.group(1)), match.group(2))
                if lastmatch != (None, None):
                    entries.append(
                        (lastmatch[0], newmatch[0] - lastmatch[0], lastmatch[1])
                    )
                lastmatch = tuple(newmatch)
        entries.append((lastmatch[0], filesize - lastmatch[0], lastmatch[1]))

    print("{:<12} {:<15} {}".format("Offset", "Est. Size", "Object"))
    for offset, size, name in entries:
        print_entry(offset, size, name, True)


if __name__ == "__main__":
    main()
