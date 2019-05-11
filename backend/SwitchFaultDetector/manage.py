#!/usr/bin/env python
import os
import sys
from threading import Thread

from backend.SwitchFaultDetector.APIService import thread_pull_data_func

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "detector.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        )
    global running
    running = True
    data_pull_thread = Thread(thread_pull_data_func, (running,))
    data_pull_thread.start()

    execute_from_command_line(sys.argv)
    running = False

    data_pull_thread.join()
