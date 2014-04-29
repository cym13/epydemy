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
from math import floor


class Virus:
    """
    This is the general class for viruses.
    """
    def __init__(self, name):
        # Game stats
        self.name  = name
        self.age   = 0
        self.money = 500
        self.research_rate       = 0
        self.research_level      = 0
        self.prev_research_level = 0

        self.target = None
        self.change_target_price = 1000

        self.danger = 0
        self.detect = 0
        self.rentab = 0
        self.spread = 0

        self.skills = []
        with open("./skills.yaml") as f:
            self.sk_list = yaml.load(f)


    def stat(self):
        """
        Used to iterate on stats or to get a value from a string
        """
        yield self.danger
        yield self.detect
        yield self.rentab
        yield self.spread


    def upgrade(self, skill):
        """
        Apply a skill patch to the virus
        """
        if skill not in self.sk_list:
            raise SkillDoesNotExist

        if self.money - self.sk_list[skill]["price"] < 0:
            raise NotEnoughMoney

        if skill in self.skills:
            raise SkillAlreadyPresent

        try:
            for each in self.sk_list[skill]["requirements"]:
                if each not in self.skills:
                    raise SkillNotAvailable
        except KeyError:
            pass

        self.money -= self.sk_list[skill]["price"]
        self.skills.append(skill)
        self.__upgrade(skill)


    def downgrade(self, skill):
        """
        Remove a skill patch from the virus
        """
        if skill not in self.skills:
            raise SkillNotPresent

        for each in self.sk_list:
            if skill in self.sk_list[each]:
                self.downgrade(each)

        self.money -= floor(self.sk_list[skill]["price"] * 0.20)
        self.skills.remove(skill)
        self.__upgrade(skill, substract=True)


    def __upgrade(self, skill, substract=False):
        """
        Avoid repetition of hard-to-read stuff for upgrade and downgrade
        """
        for each in self.sk_list[skill]["effect"]:
            value = self.sk_list[skill]["effect"][each]
            if substract:
                value *= -1

            self.__setattr__(each, self.__getattribute__(each) + value)


    def update_research(self):
        detect        = self.detect

        if self.detect >= self.research_rate:
            self.research_rate = self.detect
        else:
            self.research_rate -= (self.research_rate - self.detect) // 2

        self.prev_research_level = self.research_level
        self.research_level     += self.research_rate
        if self.research_level < 0:
            self.research_level = 0

        prev = self.prev_research_level
        if self.research_level >= 250 and prev < 250:
            raise WhiteFlag("The FBI caught you!")

        elif self.research_level >= 200 and prev < 200:
            raise EventFlag("The FBI is looking for you!")

        elif self.research_level >= 100 and prev < 100:
            raise EventFlag("Your virus is well-known!")

        elif self.research_level >= 50 and prev < 50:
            raise EventFlag("You are beginning to attract attention...")

        elif self.research_level == 0 and prev > 0:
            raise EventFlag("Nobody knows you!")


    def __str__(self):
        """
        Returns the state of the virus.
        """
        state  = "General\n"
        state += "-------\n"
        state += "Name:  %s\n" % self.name
        state += "Age:   %s\n" % self.age
        state += "Money: %s\n" % self.money
        state += "\n"
        state += "Research level: %s\n" % self.research_level
        state += "Research rate:  %s\n" % self.research_rate
        state += "\n"
        state += "Stats\n"
        state += "-----\n"
        state += "Dangerosity:   %s\n" % self.danger
        state += "Detectability: %s\n" % self.detect
        state += "Rentability:   %s\n" % self.rentab
        state += "Spreadability: %s\n" % self.spread
        state += "\n"
        state += "Skills\n"
        state += "------\n"
        for each in self.skills:
            state += each + "\n"

        return state
