import yaml
from exceptions import *

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

        with open("./countries.yaml") as f:
            self.countries = yaml.load(f)
        for each in self.countries:
            self.countries[each]["sane"] = self.countries[each]["computers"]
            self.countries[each]["infected"]       = 0
            self.countries[each]["protected"]      = 0
            self.countries[each]["destroyed"]      = 0

            self.countries[each]["research_rate"]  = 0
            self.countries[each]["research_level"] = 0

        try:
            self.countries[init_country]["infected"] = 1
        except KeyError:
            raise CountryDoesNotExist

    def step(self):
        """
        Perform one turn of spreading
        """
        money = 0
        self.sane = 0
        self.infected = 0
        self.protected = 0
        self.destroyed = 0

        inf_r  = self.virus.stat["spreadability"] * 0.01
        dest_r = self.virus.stat["dangerosity"] * 0.01
        prot_r = 1 - (self.virus.stat["detectability"] * 0.01)
        rent_r = self.virus.stat["rentability"]

        for each in self.countries:
            self.countries[each]["sane"] -= inf_r * self.countries[each]["sane"]
            self.sane += self.countries[each]["sane"]

            self.countries[each]["infected"] += (
                    inf_r * self.countries[each]["sane"] -
                    (dest_r + prot_r) * self.countries[each]["infected"])
            self.infected += self.countries[each]["infected"]

            self.countries[each]["destroyed"] += (
                                    dest_r * self.countries[each]["infected"])
            self.destroyed += self.countries[each]["destroyed"]

            self.countries[each]["protected"] += (
                                    prot_r * self.countries[each]["infected"])
            self.protected += self.countries[each]["protected"]

            money += (self.countries[each]["infected"]/
                    self.countries[each]["computers"]* rent_r*
                    self.countries[each]["money"])

        return money

    def upgrade(immunity_rate, countries=None):
        """
        Apply a virus' upgrade given its immunity rate (between -1 and 1).
        One may specify a special list of countries, default is all.
        """
        if not countries:
            countries = self.countries

        for each in countries:
            each["sane"]      += (1 - immunity_rate) * each["protected"]
            each["protected"]  = immunity_rate * each["protected"]

    def repairs(rate, countries=None):
        """
        Apply general reparations to a given rate of country's computers.
        One may specify a special list of countries, default is all.
        """
        if not countries:
            countries = self.countries

        for each in countries:
            each["sane"]      += rate * each["destroyed"]
            each["destroyed"] -= rate * each["destroyed"]

    def __str__(self):
        """
        Returns the world's state
        """
        state  = "Sane\n"
        state += "----\n"
        for each in self.countries:
            if self.countries[each]["infected"] == 0:
                state += each + " (%s)\n" % self.countries[each]["sane"]

        state += "\n"
        state += "Infected\n"
        state += "--------\n"
        for each in self.countries:
            if self.countries[each]["infected"] != 0:
                state += each +" (%s/%s)\n" % (self.countries[each]["infected"],
                                               self.countries[each]["sane"] +
                                               self.countries[each]["infected"])
        state += "\n"
        state += "Destroyed\n"
        state += "---------\n"
        for each in self.countries:
            if self.countries[each]["infected"] != 0:
                state += each +" (%s)\n" % self.countries[each]["destroyed"]

        return state
