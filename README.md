# cmd-queue

Stupid script to queue up a list of commands and trigger them
with a keystroke and to move backward and forward through the list.
I hacked this up for running sound for a show off of linux, since I
(sort of surprisingly, to me) couldn't find any decent software to
do this.

This is really dumb. Really, really dumb.

Run it with something like `./cmd_queue.py cuefile` where `cuefile`
contains something like
```
mplayer camera.wav # first
mplayer camera.wav # second
mplayer camera.wav # third
mplayer phone.wav >/dev/null 2>&1 & # play phone ringing in background
mplayer -ss 6 scratch.mp3
killall mplayer # stop phone ringing
```
