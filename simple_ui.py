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
A computer virus simulation game

Usage: epydemy [-h] [-n] FILE

Arguments:
    FILE    Save file to load, starts a new game if does not exist

Options:
    -h, --help  Print this help and exit
    -n, --new   Force a new game
                Not implemented yet
"""


import sys
from os import path
import yaml
from exceptions import *
from docopt import docopt
from virus import Virus
import world as W
from time import sleep


def play(virus, world, filename):
    """
    Main game shell and main game loop.
    """

    help_msg = """
    <enter>     Go one step forward
    help        Print this help
    patch       Open the patch panel
    save        Save the game
    quit        Quit the game
    """

    print(virus)
    print(world)

    cmd = None
    while cmd != "quit":
        cmd = input("\n> ")

        if cmd == "":
            virus.money += world.step()
            print(virus)
            print(world)

            if world.infected == 0:
                if world.sane != 0:
                    raise WhiteFlag
                elif world.sane == 0:
                    raise VictoryFlag

        elif cmd == "help":
            print(help_msg)

        elif cmd == "patch":
            patch(virus, world)

        elif cmd == "save":
            try:
                save_file(virus, world, filename)
                print("Game saved.")
            except PermissionError:
                print("The game couldn't be saved: Permission Denied")

        elif cmd != "" and cmd != "quit":
            print("Wrong command")


def patch(virus, world):
    """
    Virus modification subshell
    """

    help_msg = """
    help              Print this help
    list              List the available patches
    list own          List the present patches
    info patch        Print patch infos
    upgrade patch     Upgrade the given patch
    downgrade patch   Downgrade the given patch
    """

    cmd = None
    while cmd != "quit" and cmd != "":
        print("\nCurrent (%sBTC):" % virus.money)
        # for skill in virus.skills:
        #     print("%s (%sBTC)" % (skill,
        #                           virus.sk_list[skill]["price"] / 5))
        cmd = input(">> ")

        if cmd == "help":
            print(help_msg)

        elif cmd == "list":
            for skill in virus.sk_list:
                if skill not in virus.skills:
                    print("%s (%sBTC)" % (skill,
                                          virus.sk_list[skill]["price"]))

        elif cmd == "list own":
            for skill in virus.skills:
                print("%s (%sBTC)" % (skill,
                                      virus.sk_list[skill]["price"] / 5))

        elif cmd.startswith("info"):
            skill = cmd[5:]

            for field in virus.sk_list[skill]:
                print("%s: %s" % (field.title(), virus.sk_list[skill][field]))

        elif cmd.startswith("upgrade"):
            skill = cmd[8:]

            try:
                virus.upgrade(skill)

            except SkillDoesNotExist:
                print(skill + " does not exist")

            except SkillAlreadyPresent:
                print(skill + " is already present")

            except NotEnoughMoney:
                print("You don't have enough money to buy " + skill)

            except SkillNotAvailable:
                print("You have to unlock this skills first:")
                for each in virus.sk_list[skill]["requirements"]:
                    if each not in virus.skills:
                        print(each)

        elif cmd.startswith("downgrade"):
            skill = cmd[10:]

            try:
                virus.downgrade(skill)

            except SkillNotPresent:
                print("You don't have %s yet" % skill)

        elif cmd != "quit" and cmd != "":
            print("Wrong command")


def load_file(path):
    with open(path) as f:
        state = yaml.load(f)
        return state["virus"], state["world"], state["countries"]


def save_file(virus, world, path):
    with open(path, "w+") as f:
        f.write(yaml.dump({"virus":virus,
                           "world":world,
                           "countries": W.countries
                           }))


def main():
    args = docopt(__doc__)
    filename = args["FILE"]
    new_game = args["--new"]

    if not path.exists(filename):
        new_game = True

    if new_game:
        name = input("Enter your virus' name: ")
        virus = Virus(name)

        try:
            print("Available countries are:")
            for name in W.countries:
                print(name)
            first_country = input("Where do you want to start? ")
            print()
            world = W.World(virus, first_country)

        except CountryDoesNotExist:
            print("This country does not exist.")
            sys.exit()

    else:
        virus, world, W.countries = load_file(filename)

    try:
        play(virus, world, filename)
    except VictoryFlag:
        print("You Win!")
    except WhiteFlag:
        print("GAME OVER")


if __name__=="__main__":
    main()
