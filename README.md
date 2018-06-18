# soxnoise
## Overview
A simple, interactive, ncurses noise generator.

Soxnoise is written in Python and leverages SoX (hence the name) for its noise generation. 
It is theoretically cross-platform, but currently is only tested on Linux.

This is an curses-based program that works interactively to perform on-the-fly alteration of
parameters such as noise colour, centre frequency, reverb levels and volume.  It also supports features such as sine wave modulation to create (arguably) more pleasing noise profiles.

## Examples
While soxnoise can be controlled interactively, you can also specify all parameters on launch, e.g:

#### To play pink + brown noise with a volume of 1
soxnoise -c pinkbrown -v 1
#### To play soft pink noise with a volume of 1
soxnoise -c pink -s -v 1
#### To play white noise with reverb level of 40% 
soxnoise -c white -r 40
#### To simulate ocean type waves with pink noise and tremolo that will reduce the volume down to a minimum of 10%
soxnoise -c pink -t 0.1 -T 10 
#### To simulate ocean type waves with pink noise (minimum volume of 20% and coming every 10 seconds) and soft sine wave modulation
soxnoise -c pink -s -m 0.1 -M 20
#### To get further help
soxnoise --help

## Key bindings 
* h       : toggles the help dialogue
* 9/0 -/+ : adjusts volume
* m       : toggle mute status
* r/R     : adjusts reverb level
* f       : set tremolo frequency
* d/D     : adjusts tremolo depth
* S       : toggles sine modulation mode
* f/F     : adjusts minimum noise volume when sine modulation enabled
* s       : set sine modulation frequency when enabled


## Install
Minimal install is needed.  The only real requirement is that SoX is installed. 
A systemwide installation script that grabs dependencies for Linux installs is provided if you wish to use it.

## Screenshots
![Alt text](/screenshots/soxnoise.png?raw=true "Main view")
![Alt text](/screenshots/soxnoisehelp.png?raw=true "Help view")
