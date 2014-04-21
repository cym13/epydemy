from virus import Virus
from world import World
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


world = World(virus, "France")
class TestWorld:
    def setup(self):
        virus.__init__("test")
        world.__init__(virus, "France")

    def test_init(cls):
        assert "United-States" in list(world.countries.keys())
        assert "France" in list(world.countries.keys())

