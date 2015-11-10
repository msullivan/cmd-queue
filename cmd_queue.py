#!/usr/bin/env python3

"""Stupid script to queue up a list of commands and trigger them
with a keystroke and to move backward and forward through the list.
I hacked this up for running sound for a show off of linux, since I
(sort of surprisingly, to me) couldn't find any decent software to
do this."""

import sys
import os
import curses

def run(stdscr, cmds):
    cmds += [""]
    current = 0

    curses.def_prog_mode()

    while True:
        stdscr.clear()
        stdscr.move(0, 0)

        for i, cmd in enumerate(cmds):
            marker = " * " if current == i else "   "
            stdscr.addstr(marker + cmd + '\n')
        stdscr.refresh()

        c = stdscr.getch()
        s = chr(c)

        if s == 'n' or c == curses.KEY_DOWN or c == curses.KEY_RIGHT:
            if current + 1 < len(cmds):
                current += 1
        elif s == 'p' or c == curses.KEY_UP or c == curses.KEY_LEFT:
            if current > 0:
                current -= 1
        elif s == ' ' or s == '\n':
            if current + 1 == len(cmds): continue

            curses.reset_shell_mode()
            os.system(cmds[current])
            curses.reset_prog_mode()

            current += 1
        elif s == 'q':
            break


def main(args):
    with open(args[1]) as f:
        lines = [line.strip() for line in f]
    cmds = [x for x in lines if x and x[0] != '#']

    curses.wrapper(run, cmds)

if __name__ == '__main__':
    sys.exit(main(sys.argv))
