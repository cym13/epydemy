#!/usr/bin/env python3
#
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
Usage: cli_ui.py [options] FILE

Arguments:
    FILE    Save file

Options:
    -h, --help              Print this help and exit
    -n, --new               Force new game
    -v, --virus             Print the state of the virus
    -w, --world             Print the state of the world
    -l, --list              List available patches
    -i, --info PATCH        Print infos about the patch PATCH
    -u, --upgrade PATCH     Buy and upgrade the patch PATCH
    -d, --downgrade PATCH   Downgrade the patch PATCH and gain money
    -t, --target COUNTRY    Target the country COUNTRY
                            or none if "None" is given
"""

from docopt import docopt

def main():
    args = docopt(__doc__)
    print(args)


if __name__ == "__main__":
    main()
