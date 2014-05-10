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

Usage: server.py [-h] [-f] [-p PORT] [-n NUMBER] NAME
       server.py [-h] [-f] [-i] (-p PORT | NAME)

Arguments:
    NAME    World name

Options:
    -h, --help              Print this help and exit
    -p, --port PORT         On what port to listen. Default is 31337
    -n, --number NUMBER     Limit the number of players to 'number'
    -i, --info              Print infos on a running server
    -f, --force             Force the use of NAME even if another server is
                            registered with it
"""

import sys
import genui
import socket
import multiWorld
from virus      import Virus
from docopt     import docopt
from exceptions import *


class Server:
    """
    This is an epydemy server. It controls the world in which players act
    concurrently. It accepts commands on a UDP socket.
    """
    def __init__(self, name, port, number, force):
        """
        Initiate if possible a new server with name 'name' on port 'port' and
        with a maximum of 'number' (default 16) simultaneous players.
        """
        self.name       = name
        self.port       = port

        self.ready_nbr  = 0
        self.max_nbr    = number or 16

        self.ready      = False
        self.world      = None
        self.viruses    = {}

        self.server_list = "/tmp/epydemy.servers"
        self.update_server_list(force=force)


    def update_server_list(self, force=False, quit=False):
        """
        If quit is False, then append the name of the server into the server
        list, otherwise removes it from it.
        """
        try:
            if quit is False:
                with open(self.server_list) as f:
                    for line in f.readlines():
                        if line.startswith(self.name + " ") and not force:
                            raise ServerAlreadyExist

                with open(self.server_list, "a") as f:
                    f.write("%s localhost %s\n" % (self.name, self.port))

            else:
                with open(self.server_list, 'r') as f:
                    servers = f.readlines()

                if True not in [x.startswith(self.name + " ") for x in servers]:
                    raise ServerDoesNotExist

                with open(self.server_list, "w") as f:
                    f.writelines([x for x in servers
                                    if not x.startswith(self.name+' ')])

        except FileNotFoundError:
            open(self.server_list, "w")
            self.update_server_list()


    def handle(self, data):
        """
        Handles requests of the form:

        virus_name command [parameter]
        """
        data    = data.decode("utf-8").strip(" \n").lower().split()
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


    def pre_game(self, virus, cmd):
        """
        Pre-game commands (wait for players to come)

        Available commands are:
            init      COUNTRY   Initialize a virus in the world.
            ready               Indicate that you are ready to begin.
                                Returns the number of players still not ready.
            help                Print this help message
            quit                Quit the game.
        """
        if cmd[0] == "help":
            # Get rid of unecessary spaces before text
            return '\n'.join((x[8:] for x in self.pre_game.__doc__.split('\n')))

        elif cmd[0] == "init" and virus not in self.viruses:
            if len(cmd) == 1:
                msg  = "ERROR: Enter a country name\n"
                msg += "Are available:\n"
                for each in multiWorld.countries:
                    msg += "    %s\n" % each
                return msg

            elif len(self.viruses) < self.max_nbr:
                if cmd[1].capitalize() not in multiWorld.countries:
                    msg  = "ERROR: Unknown country\n"
                    msg += "Are available:\n"
                    for each in multiWorld.countries:
                        msg += "    %s\n" % each
                    return msg
                self.viruses[virus] = (Virus(virus), cmd[1])
                return ("SUCCESS: Virus added to the game\n"
                      + "Be sure to announce that you are ready with the "
                      + "ready command.")

            else:
                return "ERROR: The game is full"

        elif virus not in self.viruses:
            return "ERROR: Virus not initiated"

        elif cmd[0] == "ready":
            self.ready_nbr += 1

            if not self.ready and len(self.viruses) != self.ready_nbr:
                return "SUCCESS: Waiting for %s players..." % (len(self.viruses)
                                                               - self.ready_nbr)
            return "SUCCESS: Every player ready: starting the game."

        elif cmd[0] == "help":
            return self.pre_game.__doc__

        elif cmd[0] == "quit":
            self.viruses.pop(virus)
            return "SUCCESS: Your virus is no longer in the game"

        else:
            return "ERROR: Invalid command"

    def game(self, virus, cmd):
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
        if virus not in self.viruses:
            return "ERROR: Virus not initiated"

        if cmd[0] == "help":
            # Get rid of unecessary spaces before text
            return '\n'.join((x[8:] for x in self.game.__doc__.split('\n')))

        if len(cmd) == 1:
            # quit                Quit the game.
            # ready               Player ready to start the game
            # virus               Returns infos about the virus.
            # world               Returns infos about the world.
            # list                List available skills.
            if cmd[0] == "quit":
                self.viruses.pop(virus)
                return "SUCCESS: Your virus is no longer in the game"

            elif cmd[0] == "ready":
                self.ready += 1

                if self.ready < len(self.viruses):
                    v, fc = zip(self.viruses[x] for x in self.viruses)
                    self.world = MultiWorld(v, fc)
                    return "Waiting for %s players..." % len(self.viruses
                                                           - self.ready)

                return "Every player ready: starting the game."

            elif cmd[0] == "virus":
                return "SUCCESS:\n" + self.viruses[virus][0].__str__()

            elif cmd[0] == "world":
                msg  = "SUCCESS:\n"
                msg += self.world.print_country(virus)
                return msg

            elif cmd[0] == "list":
                vir = self.viruses[virus][0]
                answer = []
                for skill in self.viruses[virus][0].sk_list:
                    if vir.available(skill) and skill not in vir.skills:
                        answer.append("%s \t(%sBTC)" % (skill,
                                                  vir.sk_list[skill]["price"]))
                vir = None
                return "SUCCESS:\n" + '\n'.join(answer)

        elif len(cmd) == 2:
            # info      PATCH     Get informations about PATCH
            # upgrade   PATCH     Upgrades the virus with patch PATCH.
            # downgrade PATCH     Upgrades the virus with patch PATCH.
            # target    TARGET    Targets the country TARGET
            arg = cmd[1]
            if cmd[0] == "info":
                try:
                    vir = self.viruses[virus][0]
                    if arg not in vir.sk_list:
                        raise SkillDoesNotExist

                    answer = []
                    for field in vir.sk_list[arg]:
                        answer.append("%s: %s" % (field.title(),
                                                  vir.sk_list[arg][field]))

                    return "SUCCESS:\n" + '\n'.join(answer)

                except SkillDoesNotExist:
                    return "ERROR: This skill does not exist: %s" % arg

            elif cmd[0] == "upgrade":
                try:
                    self.viruses[virus][0].upgrade(arg)
                    return "SUCCESS: Your virus has been upgraded."

                except SkillDoesNotExist:
                    return "ERROR: %s does not exist." % arg

                except SkillAlreadyPresent:
                    return "ERROR: %s is already present." % arg

                except NotEnoughMoney:
                    return "ERROR: You don't have enough money to buy " % arg

                except SkillNotAvailable:
                    vir = self.viruses[virus][0]
                    answer = ["You have to unlock this skills first:"]
                    for each in vir.sk_list[arg]["requirements"]:
                        if each not in vir.skills:
                            answer.append(each)
                    vir = None
                    return "ERROR: " + '\n'.join(answer)

            elif cmd[0] == "downgrade":
                try:
                    self.viruses[virus][0].downgrade(arg)
                    return "SUCCESS: Your virus has been downgraded."

                except SkillNotPresent:
                    return "ERROR: You don't have %s yet" % arg

                except skillDoesNotExist:
                    return "ERROR: Wrong skill name: %s" % arg

            elif cmd[0] == "target":
                try:
                    genui.change_target(self.viruses[virus][0],
                                        multiWorld.countries,
                                        arg)
                    return "SUCCESS: Your target has changed."

                except CountryDoesNotExist:
                    return "ERROR: This country does not exist: %s" % arg

        return "ERROR: Invalid command"


    def serve_forever(self):
        """
        Server main loop
        """
        udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udp_sock.bind(("localhost", self.port))

        try:
            while True:
                data, addr = udp_sock.recvfrom(1024)
                print(addr, ":\n", data)
                sys.stdout.flush()

                command = data.decode("utf-8").strip(" \n").lower().split()[1:]

                msg  = bytes(">> " + ' '.join(command) + "\n", "utf-8")
                msg += bytes(self.handle(data), "utf-8")
                udp_sock.sendto(msg, addr)

        finally:
            udp_sock.close()
            self.update_server_list(quit=True)


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
    force  = args["--force"]

    while True:
        try:
            server = Server(name, port, number, force)
            break

        except ServerAlreadyExist:
            print("This server name is not available")
            sys.exit(1)

        except PortNotAvailable:
            print("Port", port, "not available")
            port += 1
            print("Trying on port", port)

    try:
        server.serve_forever()

    except KeyboardInterrupt:
        print("\nQuitting...")


if __name__ == "__main__":
    main()
