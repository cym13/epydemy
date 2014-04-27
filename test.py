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

import os
import simple_ui
from virus      import *
from world      import *
from exceptions import *
from nose.tools import *

virus = Virus("test")
class TestVirus:
    def setup(self):
        virus.__init__("test")

    @raises(SkillDoesNotExist)
    def test_upgrade_err_1(cls):
        virus.upgrade("None")

    @raises(NotEnoughMoney)
    def test_upgrade_err_2(cls):
        virus.money = 0
        virus.upgrade("fuzzy_code_1")

    @raises(SkillAlreadyPresent)
    def test_upgrade_err_3(cls):
        virus.money = 5000
        virus.skills.append("fuzzy_code_1")
        virus.upgrade("fuzzy_code_1")

    @raises(SkillNotAvailable)
    def test_upgrade_err_4(cls):
        virus.money = 5000
        virus.upgrade("fuzzy_code_2")

    def test_upgrade_5(cls):
        virus.money = 5000
        virus.upgrade("fuzzy_code_1")
        assert virus.skills == ["fuzzy_code_1"]
        assert virus.money == 4900

    def test_dowgrade_1(cls):
        virus.money = 0
        virus.skills = ["fuzzy_code_1"]
        virus.downgrade("fuzzy_code_1")
        assert virus.skills == []
        assert virus.money == 20

    @raises(SkillNotPresent)
    def test_dowgrade_2(cls):
        virus.downgrade("fuzzy_code_2")


world = World(virus, "Asia")
class TestWorld:
    def __init__(self):
        self.countries = countries

    def setup(self):
        virus.__init__("test")
        world.__init__(virus, "Asia")
        countries = self.countries

    def test_init(cls):
        assert "Asia" in list(countries.keys())
        assert "Africa" in list(countries.keys())

    def test_spread_1(cls):
        sane      = countries["Asia"]["sane"]
        infected  = countries["Asia"]["infected"]
        destroyed = countries["Asia"]["destroyed"]
        protected = countries["Asia"]["protected"]
        computers = countries["Asia"]["computers"]

        world.spread("Asia", 0, 0, 0)
        assert countries["Asia"]["sane"]      == sane
        assert countries["Asia"]["infected"]  == infected
        assert countries["Asia"]["destroyed"] == destroyed
        assert countries["Asia"]["protected"] == protected

    def test_spread_2(cls):
        sane      = countries["Asia"]["sane"]
        infected  = countries["Asia"]["infected"]
        destroyed = countries["Asia"]["destroyed"]
        protected = countries["Asia"]["protected"]
        computers = countries["Asia"]["computers"]

        world.spread("Asia", 0.01, 0, 0)
        assert countries["Asia"]["sane"]      <= sane
        assert countries["Asia"]["infected"]  >= infected
        assert countries["Asia"]["destroyed"] == destroyed
        assert countries["Asia"]["protected"] == protected

    def test_spread_3(cls):
        sane      = countries["Asia"]["sane"]
        infected  = countries["Asia"]["infected"]
        destroyed = countries["Asia"]["destroyed"]
        protected = countries["Asia"]["protected"]
        computers = countries["Asia"]["computers"]

        world.spread("Asia", 0.01, 0.01, 0)
        assert countries["Asia"]["sane"]      <= sane
        assert countries["Asia"]["infected"]  >= infected
        assert countries["Asia"]["destroyed"] >= destroyed
        assert countries["Asia"]["protected"] == protected


    def test_spread_4(cls):
        sane      = countries["Asia"]["sane"]
        infected  = countries["Asia"]["infected"]
        destroyed = countries["Asia"]["destroyed"]
        protected = countries["Asia"]["protected"]
        computers = countries["Asia"]["computers"]

        world.spread("Asia", 0.01, 0, 0.01)
        assert countries["Asia"]["sane"]       <= sane
        assert countries["Asia"]["infected"]   >= infected
        assert countries["Asia"]["destroyed"]  == destroyed
        assert countries["Asia"]["protected"]  >= protected


    def test_c_ratio_1(cls):
        assert c_ratio("Asia", "sane")      == (600000000, 600000001)
        assert c_ratio("Asia", "infected")  == (        1, 600000001)
        assert c_ratio("Asia", "protected") == (        0, 600000001)
        assert c_ratio("Asia", "destroyed") == (        0, 600000001)

    def test_c_ratio_2(cls):
        print( c_ratio("Asia") )
        assert c_ratio("Asia") == (0, 600000001)

    def test_money_1(cls):
        countries["Asia"]["infected"]  = 100
        countries["Asia"]["computers"] = 1000
        countries["Asia"]["money"]     = 1000
        assert world.money("Asia", 0)    == 0
        assert world.money("Asia", 0.01) == 1


class TestSimpleUI:
    def __init__(self):
        self.countries = countries

    def setup(self):
        virus.__init__("test")
        world.__init__(virus, "Asia")
        countries = self.countries

    def test_save_load(cls):
        simple_ui.save_file(virus, world, "./tmp")
        n_virus, n_world, n_countries = simple_ui.load_file("./tmp")

        assert n_virus.__str__() == virus.__str__()
        assert n_world.__str__() == world.__str__()
        assert n_countries == countries

        os.remove("./tmp")

    def test_available_1(cls):
        assert simple_ui.available("fuzzy_code_1", virus) == True
        assert simple_ui.available("fuzzy_code_2", virus) == False

    @raises(SkillDoesNotExist)
    def test_available_2(cls):
        assert simple_ui.available("something_wrong", virus)

    @raises(SkillDoesNotExist)
    def test_available_3(cls):
        assert simple_ui.available("", virus)

    def test_change_target_1(cls):
        simple_ui.change_target(virus, "target None")
        print(virus.target)
        assert virus.target is None

        simple_ui.change_target(virus, "target Asia")
        assert virus.target == "Asia"

    @raises(CountryDoesNotExist)
    def test_change_target_2(cls):
        simple_ui.change_target(virus, "target something_wrong")

