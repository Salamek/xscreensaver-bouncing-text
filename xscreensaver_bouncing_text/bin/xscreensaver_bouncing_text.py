#!/usr/bin/env python3
"""Main entry-point into the 'xscreensaver-bouncing-text' application.
This is xscreensaver-bouncing-text.
License: GPL-3.0
Website: https://github.com/Salamek/xscreensaver-bouncing-text
Usage:
    xscreensaver-bouncing-text [--text TEXT] [--windowed] [--show_fps] [--speed SPEED] [--fps FPS] [--text_color TEXT_COLOR] [--background_color BACKGROUND_COLOR] [-window-id WINDOW_ID]
    xscreensaver-bouncing-text (-h | --help)
Options:
    -window-id WINDOW_ID                           Screensaver ID of window to run in
    --windowed                                     Run in window
    -f --show_fps                                     Show FPS
    -t --text TEXT                                    Screensaver text, you can use newlines and strftime format to display datetime
    -s --speed SPEED                                  Screensaver speed [default: 1]
    -p --fps FPS                                      Screensaver FPS cap [default: 25]
    -c --text_color TEXT_COLOR                        Screensaver text color [default: #4285F4]
    -b --background_color BACKGROUND_COLOR            Screensaver background color [default: #000000]
"""

import os
import signal
import sys
import shutil
import subprocess
import datetime
from typing import Tuple, Callable
from functools import wraps
from xscreensaver_bouncing_text.Screensaver import Screensaver


from docopt import docopt

OPTIONS = docopt(__doc__)


def command(default: bool = False):
    def decorator(func):

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
        if func.__name__ not in OPTIONS and not default:
            raise KeyError('Cannot register {}, not mentioned in docstring/docopt that is not default.'.format(func.__name__))
        if func.__name__ in OPTIONS:
            command.chosen = func
        elif default:
            command.chosen = func

        return wrapped
    return decorator


@command(default=True)
def run():
    def _get_default_text_mode() -> Tuple[Callable, int]:
        def _get_default_text() -> str:
            found_xscreensaver_text_path = shutil.which('xscreensaver-text')
            if found_xscreensaver_text_path:
                return subprocess.check_output(found_xscreensaver_text_path)

            return '{}\n%H:%M:%S'.format(os.uname().nodename)

        def _default_text_callable() -> str:
            default_text = _get_default_text()
            if '%' in default_text:
                return datetime.datetime.now().strftime(default_text)

            return default_text

        return _default_text_callable, 100 if '%' in _get_default_text() else 0

    def _get_command_line_text_mode() -> Tuple[Callable, int]:
        command_line_text = OPTIONS['--text'].replace('\\n', '\n')

        def _command_line_text_callable():
            return datetime.datetime.now().strftime(command_line_text)

        return _command_line_text_callable, 100 if '%' in command_line_text else 0

    mode_list = {
        'command_line_text': _get_command_line_text_mode,
    }

    selected_mode = 'command_line_text' if OPTIONS['--text'] else None

    text_callable, callable_refresh_rate_ms = mode_list.get(selected_mode, _get_default_text_mode)()

    Screensaver(
        text_callable,
        callable_refresh_rate_ms,
        not OPTIONS['--windowed'],
        OPTIONS['--show_fps'],
        speed=int(OPTIONS['--speed']),
        fps=int(OPTIONS['--fps']),
        text_color=OPTIONS['--text_color'],
        background_color=OPTIONS['--background_color'],
        window_id=OPTIONS['WINDOW_ID']
    ).run()


def main() -> None:
    signal.signal(signal.SIGINT, lambda *_: sys.exit(0))  # Properly handle Control+C
    getattr(command, 'chosen')()  # Execute the function specified by the user.


if __name__ == '__main__':
    main()
