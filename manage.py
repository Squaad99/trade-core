#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

args = sys.argv
RUN_MODE = True
if "collectstatic" in args or "makemigrations" in args or "migrate" in args or "flush" in args or "createsuperuser" in args:
    RUN_MODE = False





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
    print("Run mode: {}".format(str(RUN_MODE)))
    execute_from_command_line(args)


if __name__ == '__main__':
    main()
