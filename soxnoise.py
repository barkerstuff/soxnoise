#!/usr/bin/env python3

# Soxnoise - A simple ncurses based noise generator that uses the power of sox
# copyright (C) 2018  Jason Barker
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

import subprocess
import argparse
from sys import exit
import curses
from curses import wrapper
import curses.panel

playerlist=['mpv','mplayer','sox']
colorlist=['pink','brown','white']

# Set up the parser
parser = argparse.ArgumentParser(description="An ncurses utility for playing noise on the terminal with SoX")
parser.set_defaults(color='pink',player='sox',volume=1,keepvolume=True)
parser.add_argument('-c','--color',help="Selects the colour of the noise to play. Available options are {0}".format(colorlist))
parser.add_argument('-d','--duration',help="Play for a specified time and then stop. The format should be a string of hh:mm:dd or an integer value in seconds",type=str)
parser.add_argument('-v','--volume',help="Sets the initial output volume. This takes a float.  Try to remain within values of 0-10 to prevent distortion",type=float)
parser.add_argument('-t','--disabletui',help="Forces the pimping ncurses interface for sox.  Defaults to on anyway",action='store_true')
args = parser.parse_args()

# Sets up default sox parameters
sox_repeats=58; sox_center=1786
sox_wave="0.00"; sox_bitrate = 16
sox_reverb = 19

# Do not alter this global. Needed so that sox knows whether or not to reinitialise the entire TUI
tui_started = False

def print_license():
    print("Soxnoise version 1, Copyright (C) 2018 Jason Barker")
    print("Soxnoise comes with ABSOLUTELY NO WARRANTY; for details see https://www.gnu.org/licenses/old-licenses/gpl-2.0.en.html")
    print("This is free software, and you are welcome to redistribute it under certain conditions.")

def main(stdscr):
    call_sox(stdscr)
    print_license()

# Stdscr is created by the sox wrapper which is wrapped around the tui initialisation
# part of call_sox(stdscr)
def tui_init(stdscr):
    # Calls the curses init function and returns the main window object
    global tui_started

    # Makes the cursor invisible
    curses.curs_set(0)

    # Disabled echo.  Not needed when using wrapper
    #curses.noecho()

    # Needed to return the timeout back to its default after the help menu thing lengthens it
    getch_timeout = 100

    # Init the cbreak mode for instant keyread. Not needed when using wrapper
    curses.cbreak()

    # Not entirely sure why or what
    stdscr.keypad(1)

    # Set stdscr to the appropriate getch timeout
    # This is defined a few lines above
    #  n.b. that the help submenu will dynamically adjust this and then restore it back to getch_timeout
    stdscr.timeout(getch_timeout)

    # Allow scrolling
    stdscr.scrollok(1)

    # Start colors if available
    if curses.has_colors():
        curses.start_color()

    # Sets up some basic colour pairs
    curses.init_pair(1,curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(2,curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(3,curses.COLOR_MAGENTA, curses.COLOR_BLACK)
    curses.init_pair(4,curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(5,curses.COLOR_WHITE, curses.COLOR_BLACK)

    # This function redraws the UI and screen
    # This is called below on the various key presses and actions to redraw the UI
    def update():
        stdscr.clear()
        # Prints the noise type and volume
        if args.color == 'white':
            stdscr.addstr(args.color,curses.color_pair(5))
            stdscr.addstr(" vol. ",curses.color_pair(4))
            stdscr.addstr(str(args.volume),curses.color_pair(4))
        if args.color == 'pink':
            stdscr.addstr(args.color,curses.color_pair(3))
            stdscr.addstr(" vol. ",curses.color_pair(4))
            stdscr.addstr(str(args.volume),curses.color_pair(4))
        if args.color == 'brown':
            stdscr.addstr(args.color,curses.color_pair(1))
            stdscr.addstr(" vol. ",curses.color_pair(4))
            stdscr.addstr(str(args.volume),curses.color_pair(4))
        # Prints the reverb level
        stdscr.addstr("  (r)everb. ",curses.color_pair(1))
        stdscr.addstr(str(sox_reverb),curses.color_pair(1))
        # Prints the center frequency
        stdscr.addstr("  (c)enterHz. ",curses.color_pair(2))
        stdscr.addstr(str(sox_center),curses.color_pair(2))

        # Refresh screen
        try:
            stdscr.noutrefresh()
            curses.doupdate()
        except Exception as E:
            stdscr.clear()
            stdscr.addstr("Term too small")

    # Let the sox call function know that tui has been started, to avoid restarting it
    tui_started = True

    # Do the first screen update in order to draw the TUI
    update()

    # This is the main loop that controls the entire TUI
    while True:

    	# Listen for input
        c = stdscr.getch()

    	# Now take user input
        global sox_reverb, sox_center
        if c == ord('q'):
            while True:
                f.kill()
                exit()

        # Adjust the volume on the fly
        elif c == ord('9') or c == ord('-'):
            if args.volume > 0.25:
                args.volume -= 0.25
            elif args.volume <= 0.25:
                args.volume = 0
            f.kill(); call_sox(stdscr); update()
        elif c == ord('0'):
            if args.volume < 30 or c == ord('='):
                args.volume += 0.25
            f.kill(); call_sox(stdscr); update()

        # M to mute
        elif c == ord('m'):
            if args.volume > 0:
                args.volume = 0.0
                #oldvol=float(args.volume)
            elif args.volume == 0.0:
                #args.volume = float(oldvol)
                args.volume = 1
            f.kill(); call_sox(stdscr); update()

        # Adjusts center frequency on the fly in Hz
        elif c == ord('c'):
            if sox_center < 4000:
                sox_center += 100
            f.kill(); call_sox(stdscr); update()
        elif c == ord('C'):
            if sox_center > 100:
                sox_center -= 100
            f.kill(); call_sox(stdscr); update()

        # Adjusts reverb
        elif c == ord('r'):
            if sox_reverb < 90:
                sox_reverb += 10
            f.kill(); call_sox(stdscr); update()
        elif c == ord('R'):
            if sox_reverb > 10:
                sox_reverb -= 10
            f.kill(); call_sox(stdscr); update()

        # Switch noise types on the fly
        elif c == ord('b'):
            args.color = 'brown'
            f.kill(); call_sox(stdscr); update()
        elif c == ord('w'):
            args.color = 'white'
            f.kill(); call_sox(stdscr); update()
        elif c == ord('p'):
            args.color = 'pink'
            f.kill(); call_sox(stdscr); update()

        # Brings up help dialog
        elif c == ord('h'):

            # Sets a longer timeout to wait for getch (since the user probably wants to read it)
            stdscr.timeout(1000000)

            # Try and except block to catch when the term gets too tiny
            try:
                stdscr.addstr(0,48,"In help")
                stdscr.addstr(2,0,"9/0 : adjusts volume")
                stdscr.addstr(3,0,"c/C : adjusts center frequency")
                stdscr.addstr(4,0,"r/R : adjusts reverb level")
                stdscr.addstr(5,0,"m : mute the audio")
                stdscr.addstr(7,0,"p/b/w : selects different noise profiles")
                stdscr.addstr(8,0," (p)ink (b)rown (w)hite",curses.color_pair(2))
                stdscr.addstr(9,0,"  press h to exit help",curses.color_pair(1))
            except:
                stdscr.clear()
                stdscr.addstr('Term too small')


            # Waits for help window to close before allowing any further updates to the screen
            b = stdscr.getch()
		
            if b == ord('h'):
                c = ''
                # Returns the timeout back to the original value
                stdscr.timeout(int(getch_timeout))
                update()

def call_sox(stdscr):
    global f, tui_started

    # If duration is specified as a starting argument then sox will receive this parameter
    #  the correct format is either hh:mm:ss or a straight integer of the desired seconds duration
    if args.duration and args.disabletui:
        subprocess_list = ['play','-b',str(sox_bitrate),'-c','2','--null','synth',str(args.duration),str(args.color)+'noise','band','-n',str(sox_center),'499','tremolo',str(sox_wave),'43','reverb',str(sox_reverb),'bass','-11','treble','-1','vol',str(args.volume)]
    elif args.duration and not args.disabletui:
        subprocess_list = ['play','-q','-b',str(sox_bitrate),'-c','2','--null','synth',str(args.duration),str(args.color)+'noise','band','-n',str(sox_center),'499','tremolo',str(sox_wave),'43','reverb',str(sox_reverb),'bass','-11','treble','-1','vol',str(args.volume)]
    elif not args.duration and not args.disabletui:
        subprocess_list = ['play','-q','-b',str(sox_bitrate),'-c','2','--null','synth',str(args.color)+'noise','band','-n',str(sox_center),'499','tremolo',str(sox_wave),'43','reverb',str(sox_reverb),'bass','-11','treble','-1','vol',str(args.volume)]
    elif not args.duration and args.disabletui:
        subprocess_list = ['play','-b',str(sox_bitrate),'-c','2','--null','synth',str(args.color)+'noise','band','-n',str(sox_center),'499','tremolo',str(sox_wave),'43','reverb',str(sox_reverb),'bass','-11','treble','-1','vol',str(args.volume)]

    # Used for subprocess debug
    #exit(" ".join(subprocess_list))

    # If TUI is disabled then keep the normal sox console output
    # Otherwise pipe it all so that only the TUI can be seen
    if args.disabletui:
        curses.endwin()
        f = subprocess.call(subprocess_list)
        curses.echo(1); curses.nocbreak(); curses.curs_set(1)
    if not args.disabletui:
        f = subprocess.Popen(subprocess_list,stderr=subprocess.PIPE,stdout=subprocess.PIPE)

    if not tui_started:
        # Starts the tui unless explicitly disabled
        if not args.disabletui:
            tui_init(stdscr)

print_license()

if __name__ == '__main__':
    try:
        wrapper(main)
    except KeyboardInterrupt:
        subprocess.call(['clear'])
        print_license()


