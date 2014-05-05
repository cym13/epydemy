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


# To change
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
        self.sane      = { x : 0 for x in zip(viruses, country) }
        self.infected  = { x : 0 for x in zip(viruses, country) }
        self.destroyed = { x : 0 for x in zip(viruses, country) }
        self.protected = { x : 0 for x in zip(viruses, country) }

        for each in zip(viruses, first_countries):
            self.infected[each] = 1
            self.viruses[each[0]].target = each[1]


    def step(self):
        """
        Perform one turn of spreading
        """
        self.virus.age += 1

        for v in self.viruses:
            inf_r  = v.spread * 0.001
            dest_r = v.danger * 0.001
            prot_r = v.detect * 0.001
            rent_r = v.rentab

            if inf_r < 0:
                inf_r = 0
            if dest_r < 0:
                dest_r = 0
            if prot_r < 0:
                prot_r = 0
            if rent_r < 0:
                rent_r = 0

            for c in countries:
                self.spread(v, c, inf_r, dest_r, prot_r)


    def money(self, country, rent_r):
        return round(countries[country]["infected"]
                         / countries[country]["computers"]
                         * rent_r
                         * countries[country]["money"])


    # This may be simplified
    def spread(self, virus, country, inf_r, dest_r, prot_r):
        """
        Core of the game mechanics
        Manages the evolution of the infection in a country
        """
        target  = virus.target

        sane      = self.sane[virus, country]
        infected  = self.sane[virus, country]
        destroyed = self.sane[virus, country]
        protected = self.sane[virus, country]

        # Asymptotic limit counter-measure
        p_sane      = sane + 1000
        p_infected  = infected
        p_destroyed = destroyed
        p_protected = protected
        computers = countries["computers"]

        # Add some randomness to the values
        inf_r  *= (random.randint(1, 10) / 30)
        dest_r *= (random.randint(1, 10) / 30)
        prot_r *= (random.randint(1, 10) / 30)

        if target == None:
            pass
        elif target == country:
            inf_r *= 2.00
        else:
            inf_r *= 0.10

        sane -= round(inf_r * p_sane)
        if sane < 0:
            sane = 0

        infected += round(inf_r  * p_sane)
        infected -= round(dest_r * p_infected)
        infected -= round(prot_r * p_infected)
        if infected > computers:
            infected = computers

        destroyed += round(dest_r * infected)
        if destroyed > computers:
            destroyed = computers

        protected += round(prot_r * infected)
        if protected > computers:
            protected = computers

        self.sane[virus, country]      = sane
        self.infected[virus, country]  = infected
        self.protected[virus, country] = protected
        self.destroyed[virus, country] = destroyed
        self.viruses[virus].money += self.money(virus, country)


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
