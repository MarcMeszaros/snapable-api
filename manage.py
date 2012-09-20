#!/usr/bin/env python
import os
import socket
import sys

if __name__ == "__main__":
    sys.path.append('../')
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "api.settings")

    # start newrelic if on athena (staging)
    if ('athena' in socket.gethostname()):
        import newrelic.agent
        newrelic.agent.initialize('newrelic.ini', 'staging')
    # start newrelic if on ares (production)
    elif ('ares' in socket.gethostname()):
        import newrelic.agent
        newrelic.agent.initialize('newrelic.ini', 'production')

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
