# xscreensaver-bouncing-text
Simple bouncing text screensaver for xscreensaver with UTF-8 support.

Demo at https://www.youtube.com/watch?v=22j96jMjcXU

# Features

* Simple installation and configuration
* Installed from repository
* Unicode support
* Option to use strftime format to show date/time
* Multiline support, just use newline character to end the line (\n)

# Installation

## Archlinux
(Use Archlinux ARM for Raspberry install)

Add repository by adding this at end of file /etc/pacman.conf

```
[salamek]
Server = https://repository.salamek.cz/arch/pub/any
SigLevel = Optional
```

and then install by running

```bash
$ pacman -Sy xscreensaver-bouncing-text
```

# Debian and derivates

Add repository by running these commands

```bash
$ wget -O - https://repository.salamek.cz/deb/salamek.gpg.key|sudo apt-key add -
$ echo "deb     https://repository.salamek.cz/deb/pub all main" | sudo tee /etc/apt/sources.list.d/salamek.cz.list
```

And then you can install a package `xscreensaver-bouncing-text`

```bash
$ apt update && apt install xscreensaver-bouncing-text
```

# Setup

After successful installation you will want to configure `xscreensaver` by editing `~/.xscreensaver` file adding this screensaver


# Usage:

```
$ xscreensaver-bouncing-text -h

Main entry-point into the 'xscreensaver-bouncing-text' application.
This is xscreensaver-bouncing-text.
License: GPL-3.0
Website: https://github.com/Salamek/xscreensaver-bouncing-text
Usage:
    xscreensaver-bouncing-text [--text=TEXT] [--windowed] [--show_fps] [--speed=SPEED] [--fps=FPS] [--text_color=TEXT_COLOR] [--background_color=BACKGROUND_COLOR]
    xscreensaver-bouncing-text (-h | --help)
Options:
    --windowed                                     Run in window
    --show_fps                                     Show FPS
    --text=TEXT                                    Screensaver text, you can use newlines and strftime format to display datetime
    --speed=SPEED                                  Screensaver speed [default: 1]
    --fps=FPS                                      Screensaver FPS cap [default: 60]
    --text_color=TEXT_COLOR                        Screensaver text color [default: #4285F4]
    --background_color=BACKGROUND_COLOR            Screensaver background color [default: #000000]
```