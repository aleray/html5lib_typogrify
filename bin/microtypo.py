#! /usr/bin/env python


# Copyright (C) 2015 Alexandre Leray

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


# Fixes French typography in HTML files
#
# Usage:
#
#     ./microtypo.py infile.md outfile.html
#     echo "<p>...</p>" | ./microtypo.py - outfile.html
#     echo "<p>...</p>" | ./microtypo.py | someotherprogramm
#     ./microtypo.py infile.md outfile.html


import codecs
import html5lib

from html5lib.filters import whitespace
from html5lib_typogrify.french.filters import hyphenate, medor, figures


def fix_french(html):
    # Using etree is important here because it does not suffer from a bug
    # where a text featuring entitities is split into various
    # adjacent text nodes.
    # (thanks html5lib folks for the tip).
    # See <https://github.com/html5lib/html5lib-python/issues/208>
    dom = html5lib.parseFragment(html, treebuilder="etree")
    walker = html5lib.getTreeWalker("etree")

    stream = walker(dom)
    stream = whitespace.Filter(stream)
    stream = medor.Filter(stream)
    stream = figures.Filter(stream)
    stream = hyphenate.Filter(stream, min_len=7, left=3, right=4)

    serializer = html5lib.serializer.HTMLSerializer(quote_attr_values=True,
            alphabetical_attributes=True,
            omit_optional_tags=False)

    return serializer.render(stream)


if __name__ == '__main__':
    import argparse
    import sys

    parser = argparse.ArgumentParser()
    parser.add_argument('infile', nargs='?', type=argparse.FileType('r'), default=sys.stdin)
    parser.add_argument('outfile', nargs='?', type=argparse.FileType('w'), default=sys.stdout)
    args = parser.parse_args()

    content = args.infile.read()
    try:
        unicode_content = content.decode("utf-8")
    except UnicodeDecodeError:
        unicode_content = content.decode("iso8559-1")

    html = fix_french(unicode_content)

    args.outfile.write(html.encode("utf-8"))
