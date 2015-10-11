# -*- coding: utf-8 -*-
import pyphen
import re
from html5lib.filters import _base


class Filter(_base.Filter):
    """
    >>> import html5lib
    >>> from html5lib.filters import sanitizer
    >>>
    >>> string = "<p>Des outils sensibles</p>"
    >>> dom = html5lib.parseFragment(string, treebuilder="dom")
    >>> walker = html5lib.getTreeWalker("dom")
    >>>
    >>> stream = walker(dom)
    >>> stream = Filter(stream)
    >>>
    >>> s = html5lib.serializer.HTMLSerializer(omit_optional_tags=False)
    >>> output = s.serialize(stream)
    >>>
    >>> print(repr(s.render(stream)))
    u'<p>Des ou\\xadtils sen\\xadsibles</p>'
    """
    def __init__(self, source, left=2, right=3):
        self.source = source
        self.dic = pyphen.Pyphen(lang='fr')
        self.dic.left = left
        self.dic.right = right

    def __iter__(self):
        psplit = re.compile(r"([^\w]+)", re.UNICODE)
        pword = re.compile(r"\A[\w]+\Z", re.UNICODE)
        blacklist = ["h1", "h2"]

        for token in _base.Filter.__iter__(self):
            type = token["type"]

            skip = False

            if token["type"] == "StartTag" and token["name"] in blacklist:
                skip = True

            if token["type"] == "EndTag" and token["name"] in blacklist:
                skip = False

            if token["type"] == "Characters" and not skip:
                data = token["data"]

                parts = []

                for word in psplit.split(data):
                    if pword.match(word):
                        parts.append(self.dic.inserted(word).replace(u'-', u'\u00AD'))
                    else:
                        parts.append(word)

                token["data"] = u"".join(parts)

            yield token


if __name__ == "__main__":
    import doctest
    doctest.testmod()
