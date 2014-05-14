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
import genui
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
        assert virus.money == 4800

    def test_dowgrade_1(cls):
        virus.money = 5000
        virus.skills = ["fuzzy_code_1"]
        virus.downgrade("fuzzy_code_1")
        assert virus.skills == []
        assert virus.money == 4960

    @raises(SkillNotPresent)
    def test_dowgrade_2(cls):
        virus.downgrade("fuzzy_code_2")

    def test_update_research_1(cls):
        virus.detect              = 10
        virus.research_rate       = 0
        virus.research_level      = 0
        virus.prev_research_level = 0

        virus.update_research()

        assert virus.detect               == 10
        assert virus.research_rate        == 10
        assert virus.research_level       == 10
        assert virus.prev_research_level  == 0

        virus.update_research()

        assert virus.detect               == 10
        assert virus.research_rate        == 10
        assert virus.research_level       == 20
        assert virus.prev_research_level  == 10

        virus.detect = 5
        virus.update_research()

        assert virus.research_rate        ==  8
        assert virus.research_level       == 28
        assert virus.prev_research_level  == 20

    @raises(WhiteFlag)
    def test_update_research_2(cls):
        virus.research_rate       = 100
        virus.research_level      = 240
        virus.prev_research_level = 200
        virus.update_research()

    @raises(EventFlag)
    def test_update_research_3(cls):
        virus.research_rate       = 50
        virus.research_level      = 190
        virus.prev_research_level = 180
        virus.update_research()

    @raises(EventFlag)
    def test_update_research_4(cls):
        virus.research_rate       = 50
        virus.research_level      = 90
        virus.prev_research_level = 80
        virus.update_research()

    @raises(EventFlag)
    def test_update_research_5(cls):
        virus.research_rate       = 50
        virus.research_level      = 40
        virus.prev_research_level = 0
        virus.update_research()

    @raises(EventFlag)
    def test_update_research_6(cls):
        virus.detect              = -10
        virus.research_rate       = -10
        virus.research_level      = 5
        virus.prev_research_level = 0
        virus.update_research()

    def test_available_1(cls):
        assert virus.available("fuzzy_code_1") == True
        assert virus.available("fuzzy_code_2") == False

    @raises(SkillDoesNotExist)
    def test_available_2(cls):
        assert virus.available("something_wrong")

    @raises(SkillDoesNotExist)
    def test_available_3(cls):
        assert virus.available("")


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


class TestGenUI:
    def __init__(self):
        self.countries = countries

    def setup(self):
        virus.__init__("test")
        world.__init__(virus, "Asia")
        countries = self.countries

    def test_save_load(cls):
        genui.save_file(virus, world, countries, "./tmp")
        n_virus, n_world, n_countries = genui.load_file("./tmp")

        assert n_virus.__str__() == virus.__str__()
        assert n_world.__str__() == world.__str__()
        assert n_countries == countries

        os.remove("./tmp")

    def test_change_target_1(cls):
        virus.money = 1000
        genui.change_target(virus, countries, "None")
        print(virus.target)
        assert virus.target is None
        assert virus.money == 0

        virus.money = 2000
        genui.change_target(virus, countries, "Asia")
        assert virus.target == "Asia"
        assert virus.money == 0

    @raises(CountryDoesNotExist)
    def test_change_target_2(cls):
        virus.money = 1000
        genui.change_target(virus, countries, "something_wrong")

    @raises(NotEnoughMoney)
    def test_change_target_3(cls):
        virus.money = 0
        genui.change_target(virus, countries, "Asia")

    def test_change_target3(cls):
        virus.money = 0

        try:
            genui.change_target(virus, countries, "Asia")
        except NotEnoughMoney:
            assert 1==1
        else:
            assert 1==2


import simple_client
path = "/tmp/test_get_server.tmp"
class TestSimpleClient:
    def setup(self):
        with open(path, "w") as f:
            f.write("true_name localhost 8000")

    def teardown(self):
        os.remove(path)

    @raises(ServerNotFound)
    def test_get_server_1(cls):
        simple_client.get_server("false_name", path)

    @raises(FileNotFoundError)
    def test_get_server_2(cls):
        simple_client.get_server("true_name", "")

    def test_get_server_3(cls):
        assert simple_client.get_server("true_name", path) == ("localhost",8000)


import cli_ui
cache = r"/tmp/epy_temp_test"
path = r"test.tmp"
last_time = 1823
class TestCliUi:
    def setup(self):
        with open(cache,"w") as f:
            f.write(str(last_time))
            f.write(path)

    def teardown(self):
        os.remove(cache)

    def test_cache(cls):
        cli_ui.write_cache(cache, last_time, path)
        print(cli_ui.read_cache(cache))
        assert cli_ui.read_cache(cache) == (last_time, 'test.tmp')


import multiWorld
virus1 = Virus("test1")
virus2 = Virus("test2")
mw = multiWorld.MultiWorld((virus1, virus2) , ("Asia", "Africa"))
class TestMultiWorld:
    def setup(self):
        virus1 = Virus("test1")
        virus2 = Virus("test2")

    def test_init(cls):
        assert mw.viruses == (virus1, virus2)

        assert mw.infected[virus1, "Asia"]    == 1
        assert mw.infected[virus1, "Africa"]  == 0
        assert mw.infected[virus2, "Africa"]  == 1
        assert mw.infected[virus2, "Asia"]    == 0

        assert mw.protected[virus1, "Asia"]   == 0
        assert mw.protected[virus1, "Africa"] == 0
        assert mw.protected[virus2, "Asia"]   == 0
        assert mw.protected[virus2, "Africa"] == 0

        assert mw.destroyed[virus1, "Asia"]   == 0
        assert mw.destroyed[virus1, "Africa"] == 0
        assert mw.destroyed[virus2, "Africa"] == 0
        assert mw.destroyed[virus2, "Asia"]   == 0

        assert mw.sane[virus1, "Asia"]   == 599999999
        assert mw.sane[virus1, "Africa"] == 100000000
        assert mw.sane[virus2, "Africa"] == 99999999
        assert mw.sane[virus2, "Asia"]   == 600000000

    def test_step(cls):
        virus1.spread = 10
        virus2.spread = 0

        mw.step()

        assert virus1.age == 1
        assert virus2.age == 1

        assert virus1.danger == 0
        assert virus1.detect == 0
        assert virus1.spread == 10
        assert virus1.rentab == 0

        assert mw.sane[virus1, "Asia"]       > 0
        assert mw.sane[virus1, "Asia"]       < 600000000
        assert mw.infected[virus1, "Asia"]   > 1
        assert mw.infected[virus1, "Asia"]   < 600000000
        assert mw.protected[virus1, "Asia"] == 0
        assert mw.destroyed[virus1, "Asia"] == 0

        assert mw.sane[virus1, "Africa"]      > 0
        assert mw.sane[virus1, "Africa"]      < 100000000
        assert mw.infected[virus1, "Africa"]  > 0
        assert mw.infected[virus1, "Africa"]  < 100000000
        assert mw.protected[virus1, "Africa"] == 0
        assert mw.destroyed[virus1, "Africa"] == 0

        assert virus2.danger == 0
        assert virus2.detect == 0
        assert virus2.spread == 0
        assert virus2.rentab == 0

        assert mw.sane[virus2, "Asia"]      == 600000000
        assert mw.infected[virus2, "Asia"]  == 0
        assert mw.protected[virus2, "Asia"] == 0
        assert mw.destroyed[virus2, "Asia"] == 0

        assert mw.sane[virus2, "Africa"]      == 99999999
        assert mw.infected[virus2, "Africa"]  == 1
        assert mw.protected[virus2, "Africa"] == 0
        assert mw.destroyed[virus2, "Africa"] == 0

    def test_money(cls):
        mw.infected[virus1, "Asia"] = 1000000000
        assert mw.money(virus1, "Asia", 0)   == 0
        assert mw.money(virus1, "Asia", 1)   == 117
        assert mw.money(virus1, "Asia", 2)   == 233
        mw.infected[virus1, "Asia"] = 1

    def test_c_ratio(cls):
        assert mw.c_ratio(virus1, "Asia", "sane")      == (599999999, 600000000)
        assert mw.c_ratio(virus1, "Asia", "infected")  == (        1, 600000000)
        assert mw.c_ratio(virus1, "Asia", "protected") == (        0, 600000000)
        assert mw.c_ratio(virus1, "Asia", "destroyed") == (        0, 600000000)

        assert mw.c_ratio(virus1, "Africa", "sane")     ==(100000000, 100000000)
        assert mw.c_ratio(virus1, "Africa", "infected") ==(        0, 100000000)
        assert mw.c_ratio(virus1, "Africa", "protected")==(        0, 100000000)
        assert mw.c_ratio(virus1, "Africa", "destroyed")==(        0, 100000000)

        assert mw.c_ratio(virus2, "Asia", "sane")      == (600000000, 600000000)
        assert mw.c_ratio(virus2, "Asia", "infected")  == (        0, 600000000)
        assert mw.c_ratio(virus2, "Asia", "protected") == (        0, 600000000)
        assert mw.c_ratio(virus2, "Asia", "destroyed") == (        0, 600000000)

        assert mw.c_ratio(virus2, "Africa", "sane")     == (99999999, 100000000)
        assert mw.c_ratio(virus2, "Africa", "infected") == (       1, 100000000)
        assert mw.c_ratio(virus2, "Africa", "protected")== (       0, 100000000)
        assert mw.c_ratio(virus2, "Africa", "destroyed")== (       0, 100000000)


import server
class TestServer:
    def setup(self):
        pass

    def test_init(cls):
        pass

    def test_update_server_list_1(cls):
        pass

    @raises(ServerAlreadyExist)
    def test_update_server_list_2(cls):
        raise ServerAlreadyExist

    def test_update_server_list_3(cls):
        pass

    def test_update_server_list_4(cls):
        pass

    @raises(ServerDoesNotExist)
    def test_update_server_list_5(cls):
        raise ServerDoesNotExist

    def test_handle_1(cls):
        pass

    def test_handle_2(cls):
        pass

    def test_pre_game_init(cls):
        pass

    def test_pre_game_ready(cls):
        pass

    def test_pre_game_quit(cls):
        pass

    def test_game_init(cls):
        pass

    def test_game_info(cls):
        pass

    def test_game_upgrade(cls):
        pass

    def test_game_downgrade(cls):
        pass

    def test_game_target(cls):
        pass

    def test_game_invalid_command(cls):
        pass

    def test_refresh(cls):
        pass

    def test_server_infos(cls):
        pass

    def test_serve_forever(self):
        pass

