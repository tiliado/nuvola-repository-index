import markdown


class MarkdownPage:
    def __init__(self, path: str):
        self.path = path
        self.markdown = markdown.Markdown(
                extensions=[
                    'meta',
                    'sane_lists',
                    'footnotes(PLACE_MARKER=$FOOTNOTES$)',
                    'fenced_code',
                    'codehilite',
                    'def_list',
                    'attr_list',
                    'abbr',
                    'admonition',
                ],
                lazy_ol=False)
        self.body = None
        self.metadata = None
        self.references = None

    def process(self):
        with open(self.path) as fh:
            data = fh.read()
        md = self.markdown
        self.body = md.convert(data)
        self.metadata = m = {}
        for key, val in md.Meta.items():
            m[key] = " ".join(val)
        self.references = md.references