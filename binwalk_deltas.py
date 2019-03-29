"""
Print deltas in binwalk output. Use like:
python binwalk-deltas.py <(binwalk BINFILE) BINFILE
"""

from errno import EPIPE
import re
import sys
import os
from functools import wraps
from sys import exit, stderr, stdout
from traceback import print_exc

import humanize


def suppress_broken_pipe_msg(f):
    @wraps(f)
    def wrapper(*args, **kwargs):

        try:
            broken_pipe_exception = BrokenPipeError
        except NameError:  # Python 2
            broken_pipe_exception = IOError

        try:
            return f(*args, **kwargs)
        except SystemExit:
            raise
        except broken_pipe_exception as exc:
            if broken_pipe_exception == IOError:
                if exc.errno != EPIPE:
                    raise
        except:
            print_exc()
            exit(1)
        finally:
            try:
                stdout.flush()
            finally:
                try:
                    stdout.close()
                finally:
                    try:
                        stderr.flush()
                    finally:
                        stderr.close()

    return wrapper


def print_entry(offset, size, name, human=False):
    if human:
        size = humanize.naturalsize(size)
    print("0x{:<10x} {:<10} {}".format(offset, size, name))


@suppress_broken_pipe_msg
def main():
    binwalk_re = re.compile(r"(\d+)\s+0x[0-9a-fA-F]+\s+(.*)\s*$")

    entries = []

    filesize = os.stat(sys.argv[2]).st_size

    with open(sys.argv[1], "r") as infile:
        lastmatch = None
        for line in infile.readlines():
            m = binwalk_re.match(line.strip())
            if m:
                newmatch = (int(m.group(1)), m.group(2))
                if lastmatch:
                    entries.append(
                        (lastmatch[0], newmatch[0] - lastmatch[0], lastmatch[1])
                    )
                lastmatch = tuple(newmatch)
        entries.append((lastmatch[0], filesize - lastmatch[0], lastmatch[1]))

    print("{:<12} {:<10} {}".format("Offset", "Est. Size", "Object"))
    for offset, size, name in entries:
        print_entry(offset, size, name, True)


if __name__ == "__main__":
    main()
