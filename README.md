# soxnoise
## Overview
A simple, interactive, ncurses noise generator.

Soxnoise is written in Python and leverages SoX (hence the name) for its noise generation. 
It is theoretically cross-platform, but currently is only tested on Linux.

This is an curses-based program that works interactively to perform on-the-fly alteration of
parameters such as noise colour, centre frequency, reverb levels and volume.  It also supports features such as sine wave modulation to create (arguably) more pleasing noise profiles.

## Examples
While soxnoise can be controlled interactively, you can also specify parameters on launch

#### To play pink + brown noise with a volume of 1
soxnoise -c pinkbrown -v 1
#### To play white noise with reverb level of 40% 
soxnoise -c white -r 40
#### To simulate ocean type waves with pink noise and tremolo
soxnoise -c pink -t 0.1 -T 10 
#### To simulate ocean type waves with pink noise (minimum volume of 20% and coming every 10 seconds) and soft sine wave modulation
soxnoise -c pink -s -m 0.1 -M 20
#### To get further help
soxnoise --help

## Install
Minimal install is needed.  The only real requirement is that SoX is installed. 
A systemwide installation script that grabs dependencies for Linux installs is provided if you wish to use it.

## Screenshots
![Alt text](/screenshots/soxnoise.png?raw=true "Main view")
![Alt text](/screenshots/soxnoisehelp.png?raw=true "Help view")
