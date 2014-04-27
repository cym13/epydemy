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


class World:
    """
    This is the world you play in.
    """
    def __init__(self, virus, init_country):
        self.virus = virus

        self.infected  = 1
        self.sane      = 0
        self.destroyed = 0
        self.protected = 0

        try:
            countries[init_country]["infected"] = 1
        except KeyError:
            raise CountryDoesNotExist


    def step(self):
        """
        Perform one turn of spreading
        """
        self.virus.age += 1
        money          = 0
        self.sane      = 0
        self.infected  = 0
        self.protected = 0
        self.destroyed = 0

        inf_r  = self.virus.spread * 0.001
        dest_r = self.virus.danger * 0.001
        prot_r = self.virus.detect * 0.001
        rent_r = self.virus.rentab

        if inf_r < 0:
            inf_r = 0
        if dest_r < 0:
            dest_r = 0
        if prot_r < 0:
            prot_r = 0
        if rent_r < 0:
            rent_r = 0

        for country in countries:
            self.spread(country, inf_r, dest_r, prot_r)

            self.sane      += countries[country]["sane"]
            self.infected  += countries[country]["infected"]
            self.destroyed += countries[country]["destroyed"]
            self.protected += countries[country]["protected"]

            money += self.money(country, rent_r)

        return money


    def money(self, country, rent_r):
        return round(countries[country]["infected"]
                         / countries[country]["computers"]
                         * rent_r
                         * countries[country]["money"])


    def spread(self, country, inf_r, dest_r, prot_r):
        """
        Core of the game mechanics
        Manages the evolution of the infection in a country
        """
        target = self.virus.target

        sane      = countries[country]["sane"]
        infected  = countries[country]["infected"]
        destroyed = countries[country]["destroyed"]
        protected = countries[country]["protected"]
        computers = countries[country]["computers"]

        # Add some randomness to the values
        inf_r  *= (random.randint(1, 10) / 30)
        dest_r *= (random.randint(1, 10) / 30)
        prot_r *= (random.randint(1, 10) / 30)

        if target == None:
            pass
        elif target == country:
            print("== %s ==" % target)
            inf_r *= 2.00
        else:
            inf_r *= 0.10

        # Asymptotic limit counter-measure
        countries[country]["sane"] += 1000

        sane -= round(inf_r * countries[country]["sane"])
        if sane < 0:
            sane = 0

        infected += round(inf_r  * countries[country]["sane"])
        infected -= round(dest_r * countries[country]["infected"])
        infected -= round(prot_r * countries[country]["infected"])
        if infected > computers:
            infected = computers

        destroyed += round(dest_r * infected)
        if destroyed > computers:
            destroyed = computers

        protected += round(prot_r * infected)
        if protected > computers:
            protected = computers

        countries[country]["sane"]      = sane
        countries[country]["infected"]  = infected
        countries[country]["destroyed"] = destroyed
        countries[country]["protected"] = protected
        countries[country]["computers"] = computers


    def upgrade(immunity_rate, country_lst=None):
        """
        Apply a virus' upgrade given its immunity rate (between -1 and 1).
        One may specify a special list of countries, default is all.
        """
        if not country_lst:
            country_lst = countries

        for each in country_lst:
            each["sane"]      += round((1 - immunity_rate) * each["protected"])
            each["protected"]  = round(immunity_rate * each["protected"])


    def repairs(rate, country_lst=None):
        """
        Apply general reparations to a given rate of country's computers.
        One may specify a special list of countries, default is all.
        """
        if not country_lst:
            countr_lst = countries

        for each in country_lst:
            each["sane"]      += round(rate * each["destroyed"])
            each["destroyed"] -= round(rate * each["destroyed"])


    def __str__(self):
        """
        Returns the world's state
        """
        max_len = max([len(x) for x in countries]) + 4

        state  = "Sane\n"
        state += "----\n"
        for each in countries:
            if countries[each]["infected"] == 0:
                state += each.ljust(max_len)
                state += " (%s\t/ %s)\n" % c_ratio(each, "sane", "protected")

        state += "\n"
        state += "Infected\n"
        state += "--------\n"
        for each in countries:
            if countries[each]["infected"] != 0:
                state += each.ljust(max_len)
                state += " (%s\t/ %s)\n"% c_ratio(each, "infected")

        state += "\n"
        state += "Destroyed\n"
        state += "---------\n"
        for each in countries:
            if countries[each]["destroyed"] != 0:
                state += each.ljust(max_len)
                state += " (%s\t/ %s)\n" % c_ratio(each, "destroyed")

        return state.rstrip('\n')
