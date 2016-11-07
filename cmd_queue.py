#!/usr/bin/env python3

"""Stupid script to queue up a list of commands and trigger them
with a keystroke and to move backward and forward through the list.
I hacked this up for running sound for a show off of linux, since I
(sort of surprisingly, to me) couldn't find any decent software to
do this."""

import sys
import os
import curses

# XXX: This should get loaded from the file or something
extra_bindings = {
    'H': 'mplayer horn.mp3',
    'M': 'killall mplayer',
}

def cmd_empty(s):
    return not s or s[0] == '#'

def inrange(cmds, idx):
    return idx >= 0 and idx < len(cmds)

def move(cmds, current, direction):
    if not inrange(cmds, current+direction): return current
    current += direction
    while cmd_empty(cmds[current]) and inrange(cmds, current+direction):
        current += direction
    return current

def system(s):
    curses.reset_shell_mode()
    os.system(s)
    curses.reset_prog_mode()


def run(stdscr, cmds):
    cmds += [""]
    current = move(cmds, -1, 1)

    curses.def_prog_mode()

    while True:
        stdscr.clear()
        stdscr.move(0, 0)

        for i, cmd in enumerate(cmds):
            marker = " * " if current == i else "   "
            stdscr.addstr(marker + cmd + '\n')
        stdscr.addstr("-------------------------------------------------\n\n")

        stdscr.refresh()

        c = stdscr.getch()
        s = chr(c)

        if s == 'n' or s == 'j' or c == curses.KEY_DOWN or c == curses.KEY_RIGHT:
            current = move(cmds, current, +1)
        elif s == 'p' or s == 'k' or c == curses.KEY_UP or c == curses.KEY_LEFT:
            current = move(cmds, current, -1)
        elif s == ' ' or s == '\n':
            system(cmds[current])
            current = move(cmds, current, +1)
        elif s == 'q':
            break
        elif s in extra_bindings:
            system(extra_bindings[s])


def main(args):
    with open(args[1]) as f:
        cmds = [line.strip() for line in f]

    curses.wrapper(run, cmds)

if __name__ == '__main__':
    sys.exit(main(sys.argv))
