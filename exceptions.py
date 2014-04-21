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

"""
Game specific exceptions.
"""

class SkillDoesNotExist(Exception):
    """
    There is no such skill
    """

class NotEnoughMoney(Exception):
    """
    There is not enough money to perform this action.
    """

class SkillAlreadyPresent(Exception):
    """
    This skill is already in the list.
    """

class SkillNotPresent(Exception):
    """
    This skill is not in the list.
    """

class SkillNotAvailable(Exception):
    """
    The skill has unmatched requirements.
    """

class CountryDoesNotExist(Exception):
    """
    There is no such country.
    """

class VictoryFlag(Exception):
    """
    This is a Victory event, feel proud !
    """

class WhiteFlag(Exception):
    """
    You can't win anymore, try again !
    """
