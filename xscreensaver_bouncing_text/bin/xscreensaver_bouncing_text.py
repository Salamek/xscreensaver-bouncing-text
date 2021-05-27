#!/usr/bin/env python3
"""Main entry-point into the 'xscreensaver-bouncing-text' application.
This is xscreensaver-bouncing-text.
License: GPL-3.0
Website: https://github.com/Salamek/xscreensaver-bouncing-text
Command details:
    run                 Run the application.
Usage:
    chromium-kiosk [--text=TEXT] [--windowed] [--show_fps]
    chromium-kiosk run [--text=TEXT] [--windowed] [--show_fps]
    chromium-kiosk (-h | --help)
Options:
    --windowed               Run in window
    --show_fps               Show FPS
    -l DIR --log_dir=DIR        Directory to log into
    --text=TEXT        Screensaver text
"""

import os
import signal
import sys
from functools import wraps
from xscreensaver_bouncing_text.Screensaver import Screensaver


from docopt import docopt

OPTIONS = docopt(__doc__)


def command(func):
    """Decorator that registers the chosen command/function.

    If a function is decorated with @command but that function name is not a valid "command" according to the docstring,
    a KeyError will be raised, since that's a bug in this script.

    If a user doesn't specify a valid command in their command line arguments, the above docopt(__doc__) line will print
    a short summary and call sys.exit() and stop up there.

    If a user specifies a valid command, but for some reason the developer did not register it, an AttributeError will
    raise, since it is a bug in this script.

    Finally, if a user specifies a valid command and it is registered with @command below, then that command is "chosen"
    by this decorator function, and set as the attribute `chosen`. It is then executed below in
    `if __name__ == '__main__':`.

    Doing this instead of using Flask-Script.

    Positional arguments:
    func -- the function to decorate
    """

    @wraps(func)
    def wrapped():
        return func()

    # Register chosen function.
    if func.__name__ not in OPTIONS:
        raise KeyError('Cannot register {}, not mentioned in docstring/docopt.'.format(func.__name__))
    if OPTIONS[func.__name__]:
        command.chosen = func
    elif func.__name__ == 'run':
        command.chosen = func

    return wrapped


@command
def run():
    def get_default_text() -> str:
        return '{}\n%H:%M:%S'.format(os.uname().nodename)

    text = OPTIONS['--text'].replace('\\n', '\n') if OPTIONS['--text'] else get_default_text()
    Screensaver(text, not OPTIONS['--windowed'], OPTIONS['--show_fps']).run()


def main() -> None:
    signal.signal(signal.SIGINT, lambda *_: sys.exit(0))  # Properly handle Control+C
    getattr(command, 'chosen')()  # Execute the function specified by the user.


if __name__ == '__main__':
    main()
