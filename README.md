# soxnoise
A simple, interactive, ncurses noise generator.

Soxnoise is written in Python and leverages SoX (hence the name) for its noise generation. 
It is theoretically cross-platform, but currently is only tested on Linux.

This is an curses-based program that works interactively to perform on-the-fly alteration of
parameters such as noise colour, centre frequency, reverb levels and volume.

Minimal install is needed.  The only real requirement is that SoX is installed.
A systemwide installation script that grabs dependencies for Linux installs is provided if you wish to use it.

![Alt text](/screenshots/soxnoise.png?raw=true "Main view")
![Alt text](/screenshots/soxnoisehelp.png?raw=true "Help view")
