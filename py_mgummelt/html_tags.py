_tags = ['a', 'b', 'body', 'br', 'button', 'div', 'form', 'head',
         'html', 'img', 'input', 'label', 'li', 'link', 'meta', 'script',
         'select', 'span', 'table', 'td', 'textarea', 'title', 'tr', 'ul']

for n in _tags:
    def wrapper(n):
        def f(*args, **kwargs):
            return _tag(n, *args, **kwargs)
        return f

    globals()[n] = wrapper(n)

def _tag(name_, c=None, **kwargs):
    if isinstance(c, tuple):
        kwargs.update(c[1])
        c = c[0]

    attrs = u' '.join(u'{}="{}"'.format(k, v) for k, v in kwargs.items() if v is not None)
    if c is None:
        return '<{} {}>'.format(name_, attrs)
    else:
        return u'<{} {}>{}</{}>'.format(name_, attrs, c, name_)
