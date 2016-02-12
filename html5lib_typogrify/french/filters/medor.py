# -*- coding: utf-8 -*-

import regex as re
from html5lib.filters import _base


CHARS = {
    'SP'      : u' ',
    'NBSP'    : u'\u00A0',
    'ENSP'    : u'\u2000',
    'EMSP'    : u'\u2001',
    'THINSP'  : u'\u2009',
    'NBTHINSP': u"\u202F",
    'LAQUO'   : u"\u00AB",
    'RAQUO'   : u"\u00BB"
}


RE_LBRAKET_MATCH = re.compile(ur"([\(\[])\s*".format(**CHARS))
RE_LBRAKET_SUB = ur"\1".format(**CHARS)

RE_RBRAKET_MATCH = re.compile(ur"\s*([\)\]])".format(**CHARS))
RE_RBRAKET_SUB = ur"\1".format(**CHARS)

RE_COMMA_OR_PERIOD_MATCH = re.compile(ur"\s*([.,])".format(**CHARS))
RE_COMMA_OR_PERIOD_SUB = ur"\1".format(**CHARS)

RE_COLUMN_MATCH = re.compile(ur"\s*(http|https|ftp)?:".format(**CHARS))
def fix_columns(match):
    if match.group(1):
        return match.group()
    else:
        return ur"{NBSP}:".format(**CHARS)

RE_PUNCT_MATCH = re.compile(ur"\s*([;!\?%])".format(**CHARS))
RE_PUNCT_SUB = ur"{NBTHINSP}\1".format(**CHARS)

RE_LAQUO_MATCH = re.compile(ur"{LAQUO}\s*".format(**CHARS))
RE_LAQUO_SUB = ur"{LAQUO}{NBTHINSP}".format(**CHARS)

RE_RAQUO_MATCH = re.compile(ur"\s*{RAQUO}".format(**CHARS))
RE_RAQUO_SUB = ur"{NBTHINSP}{RAQUO}".format(**CHARS)


class Filter(_base.Filter):
    """
    >>> import html5lib
    >>> from html5lib.filters import sanitizer
    >>>
    >>> string = u"Oui! Non  ? Regardez: un http://chien  ; un chat. 55 % 45%"
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
    """
    def __iter__(self):
        for token in _base.Filter.__iter__(self):
            type = token["type"]

            if type == "Characters":
                text = token["data"]

                text = RE_COLUMN_MATCH.sub(fix_columns, text)
                text = RE_COMMA_OR_PERIOD_MATCH.sub(RE_COMMA_OR_PERIOD_SUB, text)
                text = RE_PUNCT_MATCH.sub(RE_PUNCT_SUB, text)
                text = RE_LAQUO_MATCH.sub(RE_LAQUO_SUB, text)
                text = RE_RAQUO_MATCH.sub(RE_RAQUO_SUB, text)
                text = RE_LBRAKET_MATCH.sub(RE_LBRAKET_SUB, text)
                text = RE_RBRAKET_MATCH.sub(RE_RBRAKET_SUB, text)

                token["data"] = text

            yield token


if __name__ == "__main__":
    import doctest
    doctest.testmod()
