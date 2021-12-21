#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

from event.lib.t_core_scheduler import TCoreScheduler


def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'trade_core.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    t_scheduler = TCoreScheduler()
    args = sys.argv
    print("Args: {}".format(args))
    if "runserver" in args:
        t_scheduler.start()
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
