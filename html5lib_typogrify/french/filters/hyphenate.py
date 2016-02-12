# -*- coding: utf-8 -*-
import pyphen
import re
from html5lib.filters import _base


def hyphenate(data, right=2, left=3, min_len=5, skip_end=0):
    dic = pyphen.Pyphen(lang='fr')
    dic.left = left
    dic.right = right

    psplit = re.compile(r"([^\w]+)", re.UNICODE)
    pword = re.compile(r"\A[\w]+\Z", re.UNICODE)

    # splits sentences into words, keeping word seperators
    split = psplit.split(data)
    # records the indices of the words
    indices = [i for i, w in enumerate(split) if pword.match(w)]

    skip = skip_end * -1
    todo = indices[:skip] if skip_end > 0 and len(indices) > 0 else indices

    for i in todo:
        # if the word is long enough, hyphenates it
        if len(split[i]) >= min_len:
            split[i] = dic.inserted(split[i], u'\u00AD')

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
    def __init__(self, source, left=2, right=3, min_len=5):
        self.source = source
        self.right = right
        self.left = left
        self.min_len = 5

    def __iter__(self):
        def can_hyphen(token):
            test1 = token["name"] in block_elts
            test2 = True

            data = token['data']

            if (None, 'class') in data:
                classes = token['data'][(None, 'class')]
                test2 = not 'exergue' in classes and not 'chapeau' in classes

            return test1 and test2

        blacklist = ["h1", "h2", "h3", "figcaption", "blockquote"]
        skip = False

        block_elts = ["p", "li"]
        in_block = False

        tokens = _base.Filter.__iter__(self)

        for token in tokens:
            # Do not hyphenate inside the tags in the blacklist
            if token["type"] == "StartTag" and token["name"] in blacklist:
                skip = True

            if token["type"] == "EndTag" and token["name"] in blacklist:
                skip = False

            if token["type"] == "StartTag" and can_hyphen(token) and not skip:
                name = token["name"]

                # Collects all the tokens of the tag so we can treat its text nodes as sentences.
                stack = [token]

                while not (token["type"] == "EndTag" and token.get("name") == name):
                    token = tokens.next()
                    stack.append(token)

                # We reference the texts nodes only
                nodes = [i for i in stack if i["type"] == "Characters"]

                if len(nodes):
                    # We do not want to hyphenate the last word of a sentence.
                    # To do so we apply a different hyphenation parameters on the last text node.

                    # First we hyphenate all the text nodes except the last one
                    for i in nodes[:-1]:
                        i["data"] = hyphenate(i["data"], right=self.right, left=self.left, min_len=self.min_len)

                    # Then we hyphenate the last text node specifying we do not want to hyphenate the last word.
                    nodes[-1]["data"] = hyphenate(nodes[-1]["data"], right=self.right, left=self.left, min_len=self.min_len, skip_end=1)

                # To finish, we just yield all the accumulated tokens
                for i in stack:
                    yield i
            else:
                yield token


if __name__ == "__main__":
    import doctest
    doctest.testmod()
