"""
This script starts the whole application on OpenShift.
"""

import os

from daphne.server import Server
from django.core.management import call_command

from config.asgi import application

port = int(os.environ.get("HTTP_PORT", 8080))

# Create a Daphne server instance to serve up your application
# It needs the ASGI application callable as an argument

call_command("migrate")  # migrate database before startup
server = Server(application=application, endpoints=[f"tcp:port={port}:interface=0.0.0.0"])

server.run()
