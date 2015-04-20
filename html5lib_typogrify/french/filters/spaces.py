# -*- coding: utf-8 -*-
import regex, locale
from html5lib.filters import _base


PUNCT_REGEX = regex.compile(ur'(\w)\s*([;:!\?%])\s*')
LAQUO_REGEX = regex.compile(ur'«(\s)')
RAQUO_REGEX = regex.compile(ur'(\s)»')
NOSPACEBEFORE_REGEX = regex.compile(ur" ([\)\]\},])")
NOSPACEAFTER_REGEX = regex.compile(ur"([\(\[\{]) ")
SPACEBEFORE_REGEX = regex.compile(ur"(\w)([\(\[\{])", regex.UNICODE)
SPACEAFTER_REGEX = regex.compile(ur"([\)\]\}:,])(\w)", regex.UNICODE)
DASHES_REGEX = regex.compile(ur"([[:alpha:]])([–—])([[:alpha:]])", regex.UNICODE)
DASHES_THIN_REGEX = regex.compile(ur"(\u202F)([–—])(\u202F)", regex.UNICODE)


def fix_nospaces(text):
    """
    Removes spaces after:   [  (  {
    Removes spaces before:  ]  )  }  ,
    """
    text = NOSPACEBEFORE_REGEX.sub(ur'\1', text)
    text = NOSPACEAFTER_REGEX.sub(ur'\1', text)
    return text

def fix_punctuation(text):
    """
    Puts thin space before:   ;  :  !
    Replaces: [SPACE]?  by  [THINSP]?
    """
    text = PUNCT_REGEX.sub(ur'\1\u202F\2 ', text)
    return text


def fix_quotes(text):
    """
    Replaces space with a thin space before/after French quotation mark.
    """
    text = LAQUO_REGEX.sub(ur'«\u202F', text)
    text = RAQUO_REGEX.sub(ur'\u202F»', text)
    return text

def fix_http(text):
    """
    Remove spaces around ":" in "http://"
    """
    return text.replace(ur'http\u202F: //', 'http://')

def fix_dashes(text):
    """
    Thin spaces around &ndash; and &mdash;
    """
    text = DASHES_REGEX.sub(ur'\1\u2009\2\u2009\3', text)
    text = DASHES_THIN_REGEX.sub(ur'\u2009\2\u2009', text) # replaces non-breakable thin space by breakable thin spaces
    return text

def fix_thinspaces(text):
    """
    Replaces thin spaces with non-breakable thin spaces
    """
    return text.replace(ur'\u2009', ur'\u202F')

class Filter(_base.Filter):
    """
    >>> import html5lib
    >>> from html5lib.filters import sanitizer
    >>>
    >>> string = "Oui! Non  ? Regardez:  un chien  ;un chat. 55 % 45%"
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
    u'Oui\u202f! Non\u202f? Regardez\u202f: un chien\u202f; un chat. 55\u202f% 45\u202f% '
    """
    def __iter__(self):
        for token in _base.Filter.__iter__(self):
            type = token["type"]

            if type == "Characters":
                token["data"] = fix_punctuation(token["data"])
                token["data"] = fix_quotes(token["data"])
                token["data"] = fix_nospaces(token["data"])
                token["data"] = fix_thinspaces(token["data"])
                token["data"] = fix_http(token["data"])
                token["data"] = fix_dashes(token["data"])

            yield token


if __name__ == "__main__":
    import doctest
    doctest.testmod()
