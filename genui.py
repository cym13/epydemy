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
This contains all the logical part of user interfaces that should not be
implementation dependant.
"""

import yaml
from exceptions import *

def world_turn(virus, world):
    """
    A turn in the world
    """
    virus.money += world.step()
    if world.infected == 0:
        if world.sane != 0:
            raise WhiteFlag("Your virus was beaten up by antiviruses...")
        elif world.sane == 0:
            raise VictoryFlag("You exterminated the internet!")

    res_lvl  = virus.research_level
    prev_lvl = virus.prev_research_level

def change_target(virus, countries, target):
    virus.money -= virus.change_target_price
    virus.change_target_price += virus.change_target_price

    country = target.capitalize()
    if country == "None":
        virus.target = None
    else:
        if country in countries:
            virus.target = country
        else:
            raise CountryDoesNotExist


def load_file(path):
    with open(path) as f:
        state = yaml.load(f)
        return state["virus"], state["world"], state["countries"]


def save_file(virus, world, countries, path):
    with open(path, "w+") as f:
        f.write(yaml.dump({"virus":virus,
                           "world":world,
                           "countries": countries
                           }))


def available(skill, virus):
    if skill not in virus.sk_list:
        raise SkillDoesNotExist

    try:
        requirements = virus.sk_list[skill]["requirements"]

        for each in requirements:
            if each not in virus.skills:
                return False
        return True

    except KeyError:
        return True


