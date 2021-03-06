#!/usr/bin/env python3
#
# Copyright (c) 2014, Cédric Picard
# All rights reserved.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# We should use a cache file to remember name of last used file for not
# having to type it each time and to remember the time of the last command to
# compute the delay and the corresponding number of rounds.
#
"""
Usage: [-h] -H host -P port VIRUS COMMAND [ARGS]
       [-h] -S server VIRUS COMMAND [ARGS]

Arguments:
    VIRUS       Name of your virus
    COMMAND     Command to send
    ARGS        Falcultative argument of COMMAND

Options:
    -h, --help              Print this help and exit
    -S, --server SERVER     Connect to the local server SERVER
    -H, --host HOST         Connect to the host HOST
    -P, --port PORT         Connect on the port PORT
"""


import sys
import socket
from os import path
from exceptions import *
from docopt import docopt


def get_server(name, path):
    """
    Get a server by its name from path.
    """
    with open(path) as f:
        for line in f.readlines():
            if line.startswith(name + " "):
                host, port = line.split()[1:3]
                return host, int(port)
    raise ServerNotFound


def send(msg, host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(bytes(msg + "\n", "utf-8"), (host, port))
    return str(sock.recv(4096), "utf-8")


def main():
    args = docopt(__doc__)
    s_list = "/tmp/epydemy.servers"
    if not args["ARGS"]:
        args["ARGS"] = ""

    if args["--server"]:
        try:
            host, port = get_server(args["--server"], s_list)

        except ServerNotFound:
            print("The server was not found in the list of current servers.")
            sys.exit(1)

        except FileNotFoundError:
            print("The file was not found")
            sys.exit(1)

    else:
        host, port = args["--host"], int(args["--port"])

    msg = ' '.join((args["VIRUS"], args["COMMAND"], args["ARGS"]))
    received = send(msg, host, port)

    for line in received.splitlines():
        print(line)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nAborting")
