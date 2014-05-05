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

import yaml
import random
from collections import namedtuple
from exceptions import *


with open("./countries.yaml") as f:
    countries = yaml.load(f)

    for each in countries:
        countries[each]["sane"] = countries[each]["computers"]
        countries[each]["infected"]       = 0
        countries[each]["protected"]      = 0
        countries[each]["destroyed"]      = 0
        countries[each]["research_rate"]  = 0
        countries[each]["research_level"] = 0


def c_ratio(country, *attributes):
    total = (countries[country]["sane"]
           + countries[country]["protected"]
           + countries[country]["infected"]
           + countries[country]["destroyed"])

    value = sum([countries[country][x] for x in attributes])
    return value, total


class MultiWorld:
    """
    This is a multiplayer-oriented world.
    """
    def __init__(self, viruses, first_countries):
        self.viruses   = viruses
        self.inf_state = {x.name : for x in viruses
                            sane      = 0
                            infected  = 0
                            destroyed = 0
                            protected = 0
                            countries = {c : 0 for c in countries}
                            }


    def step(self):
        """
        Perform one turn of spreading
        """


    def money(self, country, rent_r):
        return round(countries[country]["infected"]
                         / countries[country]["computers"]
                         * rent_r
                         * countries[country]["money"])


    # To change
    def spread(self, virus, country, inf_r, dest_r, prot_r):
        """
        Core of the game mechanics
        Manages the evolution of the infection in a country
        """

    # To change
    def upgrade(virus, immunity_rate, country_lst=None):
        """
        Apply a virus's upgrade given its immunity rate (between -1 and 1).
        One may specify a special list of countries, default is all.
        """


    # To change
    def repairs(virus, rate, country_lst=None):
        """
        Apply general reparations to a given rate of country's computers.
        One may specify a special list of countries, default is all.
        """


    # To change
    def __str__(self):
        """
        Returns the world's state
        """
