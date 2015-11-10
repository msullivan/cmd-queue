#!/usr/bin/env python3

"""Stupid script to queue up a list of commands and trigger them
with a keystroke and to move backward and forward through the list.
I hacked this up for running sound for a show off of linux, since I
(sort of surprisingly, to me) couldn't find any decent software to
do this."""

# I am not proud of any of this code.

import sys
import os
import tty, termios

def run(cmds, old):
    cmds += [""]
    current = 0

    while True:
        os.system('clear') # lurr.
        tty.setraw(sys.stdout.fileno())

        for i, cmd in enumerate(cmds):
            marker = " * " if current == i else "   "
            print(marker + cmd, end='\r\n')

        s = sys.stdin.read(1)

        # A, B, C, D get sent in as the second key for the arrows...
        # XXX: This is no way to run a railway
        if s == 'n' or s == 'B' or s == 'C':
            if current + 1 < len(cmds):
                current += 1
        elif s == 'p' or s == 'A' or s == 'D':
            if current > 0:
                current -= 1
        elif s == ' ' or s == '\r':
            if current + 1 == len(cmds): continue

            # Leave raw mode so the command we are running works right
            termios.tcsetattr(sys.stdout.fileno(), termios.TCSADRAIN, old)
            os.system(cmds[current])

            current += 1
        elif s == 'q':
            break


def main(args):
    with open(args[1]) as f:
        lines = [line.strip() for line in f]
    cmds = [x for x in lines if x and x[0] != '#']
    old = termios.tcgetattr(sys.stdout.fileno())

    try:
        run(cmds, old)
    finally:
        termios.tcsetattr(sys.stdout.fileno(), termios.TCSADRAIN, old)


if __name__ == '__main__':
    sys.exit(main(sys.argv))
