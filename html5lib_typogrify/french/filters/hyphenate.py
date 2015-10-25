# -*- coding: utf-8 -*-
import pyphen
import re
from html5lib.filters import _base


def hyphenate(data, right=2, left=3, skip_end=0):
    dic = pyphen.Pyphen(lang='fr')
    dic.left = left
    dic.right = right

    psplit = re.compile(r"([^\w]+)", re.UNICODE)
    pword = re.compile(r"\A[\w]+\Z", re.UNICODE)

    split = psplit.split(data)
    indices = [i for i, w in enumerate(split) if pword.match(w)]

    skip = skip_end * -1
    todo = indices[:skip] if skip_end > 0 and len(indices) > 0 else indices

    for i in todo:
        split[i] = dic.inserted(split[i]).replace(u'-', u'\u00AD')

    return u"".join(split)


class Filter(_base.Filter):
    """
    >>> import html5lib
    >>> from html5lib.filters import sanitizer
    >>>
    >>> string = "<p>incroyablement sensible</p><figcaption><p>Des outils <em>incroyablement</em> rugueux et sensibles.</p></figcaption>"
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
        self.right = right
        self.left = left

    def __iter__(self):
        def can_hyphen(token):
            test1 = token["name"] in block_elts
            test2 = True

            data = token['data']

            if (None, 'class') in data:
                classes = token['data'][(None, 'class')]
                test2 = not 'exergue' in classes and not 'chapeau' in classes

            return test1 and test2

        blacklist = ["h1", "h2", "h3", "figcaption"]
        skip = False

        block_elts = ["p", "li"]
        in_block = False

        tokens = _base.Filter.__iter__(self)

        for token in tokens:
            if token["type"] == "StartTag" and token["name"] in blacklist:
                skip = True

            if token["type"] == "EndTag" and token["name"] in blacklist:
                skip = False

            if token["type"] == "StartTag" and can_hyphen(token) and not skip:
                name = token["name"]
                stack = [token]

                while not (token["type"] == "EndTag" and token.get("name") == name):
                    token = tokens.next()
                    stack.append(token)

                nodes = [i for i in stack if i["type"] == "Characters"]

                if len(nodes):
                    for i in nodes[:-1]:
                        i["data"] = hyphenate(i["data"], right=self.right, left=self.left)

                    nodes[-1]["data"] = hyphenate(nodes[-1]["data"], right=self.right, left=self.left, skip_end=1)

                for i in stack:
                    yield i
            else:
                yield token


if __name__ == "__main__":
    import doctest
    doctest.testmod()
