HTML5Lib Typogrify
==================

A set of filters to correct common typographical mistakes.


Installation
------------

    pip install git+git://github.com/aleray/html5lib_typogrify.git


Usage
-----

    >>> import html5lib
    >>> from html5lib_typogrify.french.filters import ellipsis 
    >>> from html5lib_typogrify.french.filters import spaces 
    >>>
    >>> string = "Oui! Non ? Regardez:  quelle horreur  ;beurk.... Bon."
    >>> dom = html5lib.parse(string, treebuilder="dom")
    >>> walker = html5lib.getTreeWalker("dom")
    >>>
    >>> stream = walker(dom)
    >>> stream = ellipsis.Filter(stream)
    >>> stream = spaces.Filter(stream)
    >>>
    >>> s = html5lib.serializer.HTMLSerializer()
    >>> output = s.serialize(stream)
    >>>
    >>> print(repr(s.render(stream)))
    u'Oui\u202f! Non\u202f? Regardez\u202f: quelle horreur\u202f; beurk\u2026 Bon.'
