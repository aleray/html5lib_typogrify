import re
from html5lib.filters import _base


ELLIPSIS_REGEX = re.compile(r"\.{3,}")
SPACE_REGEX = re.compile(ur"\u2026(\w)")


def fix_ellipsis(text):
    text = ELLIPSIS_REGEX.sub(ur'\u2026', text)
    text = SPACE_REGEX.sub(ur'\u2026 \1', text)
    return text


class Filter(_base.Filter):
    """
    >>> import html5lib
    >>> from html5lib.filters import sanitizer
    >>>
    >>> string = "La suite.... au prochain article"
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
    u'La suite\u2026 au prochain article'
    """
    def __iter__(self):
        for token in _base.Filter.__iter__(self):
            type = token["type"]

            if type == "Characters":
                token["data"] = fix_ellipsis(token["data"])

            yield token


if __name__ == "__main__":
    import doctest
    doctest.testmod()
