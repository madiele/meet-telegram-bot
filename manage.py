#!/usr/bin/env python
import os
import sys
from django.utils.translation import gettext_lazy as _

if __name__ == "__main__":

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "letsMeetBot.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
