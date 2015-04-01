import re
from html5lib.filters import _base


EN_DASH_REGEX = re.compile(r"--")
EM_DASH_REGEX = re.compile(r"---")


def fix_dashes(text):
    text = EM_DASH_REGEX.sub(ur'\u2014', text)
    text = EN_DASH_REGEX.sub(ur'\u2013', text)
    return text


class Filter(_base.Filter):
    """
    >>> import html5lib
    >>> from html5lib.filters import sanitizer
    >>>
    >>> string = "Le tiret cadratin --- et le tiret demi-cadratin --"
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
    u'Le tiret cadratin \u2014 et le tiret demi-cadratin \u2013'
    """
    def __iter__(self):
        for token in _base.Filter.__iter__(self):
            type = token["type"]

            if type == "Characters":
                token["data"] = fix_dashes(token["data"])

            yield token


if __name__ == "__main__":
    import doctest
    doctest.testmod()
