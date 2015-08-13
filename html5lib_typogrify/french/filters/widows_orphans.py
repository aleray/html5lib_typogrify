# -*- coding: utf-8 -*-
import regex, locale
from html5lib.filters import _base


class Filter(_base.Filter):
    """
    >>> import html5lib
    >>> from html5lib.filters import sanitizer
    >>>
    >>> string = "<p>In typesetting, widows and orphans are words or short lines at the beginning or end of a paragraph</p>"
    >>> dom = html5lib.parse(string, treebuilder="dom")
    >>> walker = html5lib.getTreeWalker("dom")
    >>>
    >>> stream = walker(dom)
    >>> stream = Filter(stream)
    >>>
    >>> s = html5lib.serializer.HTMLSerializer()
    >>> output = s.serialize(stream)
    >>>
    >>> print(repr(s.render(stream)))
    u'<p>In\u00a0typesetting,\u00a0widows and orphans are words or short lines at the beginning or end of\u00a0a\u00a0paragraph'
    """
    def __init__(self, source, widows=2, orphans=2):
        self.source = source
        self.widows = widows
        self.orphans = orphans

    def __iter__(self):
        in_p = False

        for token in _base.Filter.__iter__(self):
            type = token["type"]


            if token["type"] == "StartTag" and token["name"] == "p":
                in_p = True

            elif token["type"] == "EndTag" and token["name"] == "p":
                in_p = False

            if token["type"] == "Characters" and in_p:
                data = token["data"].replace(ur' ', ur'\u00A0', self.orphans)
                data = data[::-1].replace(ur' ', ur'\u00A0', self.widows)
                token["data"] = data[::-1]

            yield token


if __name__ == "__main__":
    import doctest
    doctest.testmod()
