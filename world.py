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
        money          = 0
        self.sane      = 0
        self.infected  = 0
        self.protected = 0
        self.destroyed = 0

        inf_r  = self.virus.stat["spread"] * 0.01
        dest_r = self.virus.stat["danger"] * 0.01
        prot_r = self.virus.stat["detect"] * 0.01
        rent_r = self.virus.stat["rentab"]

        for each in countries:
            # add a if to avoid the case of negative sane
            countries[each]["sane"] -= round(inf_r * countries[each]["sane"])
            if countries[each]["sane"] < 0 :
                countries[each]["sane"] = 0

            countries[each]["infected"]  += round(inf_r
                                                * countries[each]["sane"]
                                                - (dest_r + prot_r)
                                                * countries[each]["infected"])

            if countries[each]["infected"] > countries[each]["computers"]:
                countries[each]["infected"] = countries[each]["computers"]

            countries[each]["destroyed"] += round(dest_r
                                                * countries[each]["infected"])

            if countries[each]["destroyed"] > countries[each]["computers"]:
                countries[each]["destroyed"] = countries[each]["computers"]

            countries[each]["protected"] += round(prot_r
                                                * countries[each]["infected"])

            if countries[each]["protected"] > countries[each]["computers"]:
                countries[each]["protected"] = countries[each]["computers"]

            self.sane      += countries[each]["sane"]
            self.infected  += countries[each]["infected"]
            self.destroyed += countries[each]["destroyed"]
            self.protected += countries[each]["protected"]

            money += round(countries[each]["infected"]
                         / countries[each]["computers"]
                         * rent_r
                         * countries[each]["money"])

        return money


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
