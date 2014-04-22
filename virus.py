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
        self.name = name
        self.age = 0
        self.money = 1000
        self.research_rate = 0
        self.research_level = 0

        # Skill stats
        self.stat = {"danger": 0,
                     "detect": 0,
                     "rentab": 0,
                     "spread": 0}

        self.skills = []
        with open("./skills.yaml") as f:
            self.sk_list = yaml.load(f)


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

        for each in self.sk_list[skill]["effect"]:
            # This one is really abused... I should think this all again.
            self.stat[each] += self.sk_list[skill]["effect"][each]


    def downgrade(self, skill):
        """
        Remove a skill patch from the virus
        """
        if skill not in self.skills:
            raise SkillNotPresent

        for each in self.sk_list:
            if skill in self.sk_list[each]:
                self.downgrade(each)

        self.money += floor(self.sk_list[skill]["price"] * 0.20)
        self.skills.remove(skill)

        for each in self.sk_list[skill]["effect"]:
            self.stat[each] -= self.sk_list[skill]["effect"][each]

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
        state += "Research level: %s\n" % self.research_rate
        state += "Research rate:  %s\n" % self.research_level
        state += "\n"
        state += "Stats\n"
        state += "-----\n"
        state += "Dangerosity:   %s\n" % self.stat["danger"]
        state += "Detectability: %s\n" % self.stat["detect"]
        state += "Rentability:   %s\n" % self.stat["rentab"]
        state += "Spreadability: %s\n" % self.stat["spread"]
        state += "\n"
        state += "Skills\n"
        state += "------\n"
        for each in self.skills:
            state += each + "\n"

        return state
