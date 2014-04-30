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

"""
Usage: cli_ui.py [options] [-n] FILE
       cli_ui.py [options] [FILE]

Arguments:
    FILE    Save file

Options:
    -h, --help              Print this help and exit
    -d, --downgrade PATCH   Downgrade the patch PATCH and gain money
    -i, --info PATCH        Print infos about the patch PATCH
    -l, --list              List available patches
    -n, --new               Force new game
    -u, --upgrade PATCH     Buy and upgrade the patch PATCH
    -v, --virus             Print the state of the virus
    -w, --world             Print the state of the world
    -t, --target COUNTRY    Target the country COUNTRY
                            or none if "None" is given
"""
import sys
#import yaml
import genui
from time import time
import world as W
from os import path
from virus import Virus
from docopt import docopt
from exceptions import *
from simple_ui import choose_country

def uinput(prompt):
    """
    Function to use to get user input, strip it and lower it systematically
    """
    return input(prompt).strip().lower()


def new_game(file):


    name = uinput("Enter your virus' name: ")
    virus = Virus(name)

    try:
        world = W.World(virus, choose_country())
    except CountryDoesNotExist:
        print("This country does not exist.")
        sys.exit()
    try:
        genui.save_file(virus, world, W.countries, file)
        print("Game saved.")
    except PermissionError:
        print("The game couldn't be saved: Permission Denied")

    return virus, world, W.countries


def load_game(file):
        if not path.exists(file):
            create = input("This Save file doesn't exist, "
                         + "do you want to create it ?(y/n)").strip().lower()
            if create == 'y':
                new_game(file)
            else:
                sys.exit()

        else:
            return genui.load_file(file)


def print_patch(skill, virus):
    try:
        if skill not in virus.sk_list:
            raise SkillDoesNotExist

        for field in virus.sk_list[skill]:
            print("%s: %s" % (field.title(),
                                    virus.sk_list[skill][field]))

    except SkillDoesNotExist:
        print("This skill does not exist: %s" % skill)


def print_list(virus):
    for skill in virus.sk_list:
        if skill not in virus.skills and virus.available(skill):
            print("%s \t(%sBTC)" % (skill,
                                        virus.sk_list[skill]["price"]))


def upgrade(skill, virus):
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


def downgrade(skill, virus):
    try:
        virus.downgrade(skill)

    except SkillNotPresent:
        print("You don't have %s yet" % skill)
    except skillDoesNotExist:
        print("Wrong skill name: %s" % skill)


def target(country, virus):
    try:
        if country == "None":
            print("Country name missing")
        else:
            genui.change_target(virus, W.countries, country)

    except CountryDoesNotExist:
        print("This country does not exist: %s" % country)


def main():
    #raise CountryDoesNotExist
    args = docopt(__doc__)
    #print(args)
    file = args["FILE"]
    patch = args["--info"]
    list = args["--list"]
    upgrade_skill = args["--upgrade"]
    downgrade_skill = args["--downgrade"]
    target_country = args["--target"]
    cache = r"/tmp/epy_temp"
    current_time = round(time())
    slice_time = 3
    last_time = current_time
    tfile = ""

    if path.exists(cache):
        with open(cache, "r") as f:
            last_time = int(f.readline())
            tfile = f.readline()



    if args["--new"]:
        virus, world, W.countries = new_game(file)
        tfile = file
    else:
        if file == None:
            virus, world, W.countries = load_game(tfile)
            file = tfile
        else:
            virus, world, W.countries = load_game(file)
            tfile = file


    with open(cache, "w") as tmp:
        tmp.write(str(current_time) +"\n")
        tmp.write(file)

    n_step = (current_time - last_time)//slice_time
    for i in range(n_step):
        genui.world_turn(virus, world)
#    game_data = (virus, world, W.countries)

    if patch:
        print_patch(patch, virus)
    elif list:
        print_list(virus)
    elif upgrade_skill:
        upgrade(upgrade_skill, virus)
    elif downgrade_skill:
        downgrade(downgrade_skill, virus)
    elif args["--virus"]:
        print(virus)
    elif args["--world"]:
        print(world)
    elif target_country:
        target(target_country, virus)

    genui.save_file(virus, world, W.countries, tfile)
    sys.exit()


if __name__ == "__main__":
    main()
