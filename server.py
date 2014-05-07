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
"""
Epidemy game server

Usage: server.py [-h] [-p PORT] [-n NUMBER] NAME
       server.py [-h] [-i] (-p PORT | NAME)

Arguments:
    NAME    World name

Options:
    -h, --help              Print this help and exit
    -p, --port PORT         On what port to listen. Default is 31337
    -n, --number NUMBER     Limit the number of players to 'number'
    -i, --info              Print infos on a running server
"""

import sys
import socket
import multiWorld
from docopt import docopt

class Server:
    """
    This is an epydemy server. It controls the world in which players act
    concurrently. It accepts commands on a UDP socket.
    """
    def __init__(self, name, port, number):
        """
        Initiate if possible a new server with name 'name' on port 'port' and
        with a maximum of 'number' simultaneous players.
        """
        self.name       = name
        self.port       = port

        self.ready_nbr  = 0
        self.max_nbr    = number

        self.ready      = False
        self.world      = None
        self.viruses    = {}


    def update_server_list(self, quit=False):
        """
        If quit is False, then append the name of the server into the server
        list, otherwise removes it from it.
        """


    def handle(self, data):
        """
        Handles requests of the form:

        virus_name command [parameter]
        """
        data    = str(data).strip().lower().split()
        virus   = data[0]
        command = data[1:]

        if len(self.viruses) != 0 and len(self.viruses) == self.ready_nbr:
            v, fc = zip(*(self.viruses[x] for x in self.viruses))
            self.world = multiWorld.MultiWorld(v, fc)
            self.ready = True

        if not self.ready:
            handler = self.pre_game
        else:
            handler = self.game

        return handler(virus, command)


    def pre_game(self, virus, command):
        """
        Computes pre-game commands (wait for players to come)


        Available commands are:
            init      COUNTRY   Initialize a virus in the world.
            ready               Indicate that you are ready to begin.
                                Returns the number of players still not ready.
        """
        return "hello"


    def game(self, virus, command):
        """
        Computes game commands

        Available commands are:
            quit                Quit the game.
            virus               Returns infos about the virus.
            world               Returns infos about the world.
            list                List available skills.
            info      PATCH     Get informations about PATCH
            upgrade   PATCH     Upgrades the virus with patch PATCH.
            downgrade PATCH     Upgrades the virus with patch PATCH.
            target    TARGET    Targets the country TARGET
                                or none if "None" is given.
        """


    def serve_forever(self):
        """
        Server main loop
        """
        udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udp_sock.bind(("localhost", self.port))

        while True:
            data, addr = udp_sock.recvfrom(1024)
            print(addr, ":\n", data)
            sys.stdout.flush()
            udp_sock.sendto(bytes(self.handle(data), "utf-8"), addr)

        udp_sock.close()


    def infos(self, identifier):
        """
        Print infos about a server known by 'identifier'.
        'identifier' can be a string (the server's name) or an integer (the
        server's port).
        """
        with open(self.path) as f:
            for line in f.readlines():
                data = line.split()
                if identifier in data:
                    return data


def main():
    args   = docopt(__doc__)
    name   = args["NAME"]
    port   = args["--port"] or 31337
    number = args["--number"] or None

    server = Server(name, port, number)
    server.serve_forever()


if __name__ == "__main__":
    main()
