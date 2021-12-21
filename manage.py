#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

from event.lib.t_core_scheduler import TCoreScheduler

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': ('%(asctime)s [%(process)d] [%(levelname)s] ' +
                       'pathname=%(pathname)s lineno=%(lineno)s ' +
                       'funcname=%(funcName)s %(message)s'),
            'datefmt': '%Y-%m-%d %H:%M:%S'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        }
    },
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'logging.NullHandler',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        }
    },
    'loggers': {
        'testlogger': {
            'handlers': ['console'],
            'level': 'INFO',
        }
    }
}

def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'trade_core.settings')
    import logging
    logger = logging.getLogger('testlogger')
    logger.info('This is a simple log message')
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
    if "migrate" not in args:
        print("Here123")
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
