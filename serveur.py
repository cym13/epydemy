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
"""
Epidemy game server

Usage: serveur.py [-h] [-p PORT] [-n NUMBER] NAME
       serveur.py [-h] [-i] (-p PORT | NAME)

Arguments:
    NAME    World name

Options:
    -h, --help              Print this help and exit
    -p, --port PORT         On what port to listen. Default is 31337
    -n, --number NUMBER     Limit the number of players to 'number'
    -i, --info              Print infos on a running server
"""

import sys
import genui
import threading
import socketserver
from virus      import Virus
from docopt     import docopt
from exceptions import *


def infos(identifier):
    """
    Print infos about a serveur known by 'identifier'.
    'identifier' can be a string (the server's name) or an integer (the
    server's port).
    """


class Server(socketserver.BaseRequestHandler):
    """
    This is an epydemy server. It controls the world in which players act
    concurrently. It accepts commands on a UDP socket.
    """
    def __init__(self, name, port, number):
        """
        Initiate if possible a new server with name 'name' on port 'port' and
        with a maximum of 'number' simultaneous players.
        """
        self.name = name
        self.port = port

        if number is None:
            number = 100
        self.max_number = number

        self.viruses = {}
        self.world   = MultiWorld(viruses)

    def handler(self):
        """
        Handles requests of the form:

        virus_name command [parameter]

        Available commands are:
            init                Initialize a virus in the world.
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
        socket = self.request[1]

        data   = self.request[0].strip().split()
        if len(data) < 2:
            answer = "ERROR: Invalid command"
        else:
            virus = data[0]
            cmd   = data[1]
            args  = None
            if len(data) > 2:
                args  = data[2:]
            answer = self.compute(virus, cmd, args)

        socket.sendto(answer, self.client_address)


    def compute(self, virus, cmd, args):
        """
        Computes the command 'cmd' with the arguments 'args' from 'virus'.
        """
        cmd = cmd.lower()

        if cmd == "init" and virus not in self.viruses:
            if len(self.viruses) < self.max_number:
                self.viruses[virus] = Virus(virus)
                return "SUCCESS: Virus added to the game"
            else:
                return "ERROR: The game is full"

        elif virus not in self.viruses:
            return "ERROR: Virus not initiated"

        if len(cmd) == 1:
            """
            quit                Quit the game.
            virus               Returns infos about the virus.
            world               Returns infos about the world.
            list                List available skills.
            """
            if cmd == "quit":
                self.viruses.pop(virus)
                return "SUCCESS: Your virus is no longer in the game"

            elif cmd == "virus":
                return "SUCCESS: " + self.viruses[virus].__str__

            elif cmd == "world":
                return "SUCCESS: " + self.world.__str__

            elif cmd == "list":
                vir = self.viruses[virus]
                answer = []
                for skill in self.viruses[virus].sk_list:
                    if vir.available(skill) and skill not in vir.skills:
                        answer.append("%s \t(%sBTC)" % (skill,
                                                  vir.sk_list[skill]["price"]))
                vir = None
                return "SUCCESS: " + '\n'.join(answer)

        elif len(cmd) == 2:
            """
            info      PATCH     Get informations about PATCH
            upgrade   PATCH     Upgrades the virus with patch PATCH.
            downgrade PATCH     Upgrades the virus with patch PATCH.
            target    TARGET    Targets the country TARGET
            """
            arg = cmd[1]
            if cmd == "info":
                try:
                    vir = self.viruses[virus]
                    if arg not in vir.sk_list:
                        raise SkillDoesNotExist

                    answer = []
                    for field in vir.sk_list[arg]:
                        answer.append("%s: %s" % (field.title(),
                                                  vir.sk_list[arg][field]))

                    return "SUCCESS: " + '\n'.join(answer)

                except SkillDoesNotExist:
                    return "ERROR: This skill does not exist: %s" % arg

            elif cmd == "upgrade":
                try:
                    self.viruses[virus].upgrade(arg)
                    return "SUCCESS: Your virus has been upgraded."

                except SkillDoesNotExist:
                    return "ERROR: %s does not exist." % arg

                except SkillAlreadyPresent:
                    return "ERROR: %s is already present." % arg

                except NotEnoughMoney:
                    return "ERROR: You don't have enough money to buy " % arg

                except SkillNotAvailable:
                    vir = self.viruses[virus]
                    answer = ["You have to unlock this skills first:"]
                    for each in vir.sk_list[arg]["requirements"]:
                        if each not in vir.skills:
                            answer.append(each)
                    vir = None
                    return "ERROR: " + '\n'.join(answer)

            elif cmd == "downgrade":
                try:
                    self.viruses[virus].downgrade(arg)
                    return "SUCCESS: Your virus has been downgraded."

                except SkillNotPresent:
                    return "ERROR: You don't have %s yet" % arg

                except skillDoesNotExist:
                    return "ERROR: Wrong skill name: %s" % arg

            elif cmd == "target":
                try:
                    genui.change_target(self.viruses[virus],
                                        self.countries,
                                        arg)
                    return "SUCCESS: Your target has changed."

                except CountryDoesNotExist:
                    return "ERROR: This country does not exist: %s" % arg

        return "ERROR: Invalid command"


def main():
    args   = docopt(__doc__)
    name   = args["NAME"]
    port   = args["--port"] or 31337
    number = args["--number"] or None

    if args["--info"]:
        try:
            if name:
                infos(name)
            else:
                infos(port)
        except ServerDoesNotExists:
            print("Server does not exist")
            sys.exit(1)

    while True:
        try:
            server = Server(name, port, number)
            break

        except ServerAlreadyExists:
            print("This server name is not available")
            sys.exit(1)

        except PortNotAvailable:
            port += 1

    # Should do some sort of error catching there
    print("Initiating serveur on port " + str(port))
    server.serve_forever()


if __name__ == "__main__":
    main()
