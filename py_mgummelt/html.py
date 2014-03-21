from urlparse import urlparse

def page(title, c, css=[], js=[], less=[]):
    def html():
        return tag('html',
                   head() + body(c),
                   lang='en')

    def css_link(href):
        if not urlparse(href).netloc:
            href = 'static/css/{}.css'.format(href)

        return tag('link', '',
                   rel='stylesheet',
                   type='text/css',
                   href=href)

    def head():
        return tag('head',
                   tag('title', title) +
                   tag('meta', '', charset='utf8') +
                   ''.join(map(css_link, css)) +
                   ''.join(map(script, js)))

    return '<!DOCTYPE html>' + html()

def script(src):
    return tag('script', '', src='static/js/{}.js'.format(src))

def select(name, options):
    return tag('select',
               ''.join(tag('option', opt, value=opt) for opt in options),
               name=name)

def a(href, text=None, **kwargs):
    return tag('a', text if text is not None else href, href=href, **kwargs)

def table(rows, **kwargs):
    def td(cell):
        if hasattr(cell, '__iter__'):
            return tag('td', cell[0], **cell[1])
        else:
            return tag('td', cell)
    def tr(row):
        if len(row) == 2 and isinstance(row[1], dict):
            return tag('tr', ''.join(map(td, row[0])), **row[1])
        else:
            return tag('tr', ''.join(map(td, row)))

    return tag('table', ''.join(map(tr, rows)), **kwargs)

def li(c):
    return tag('li', c)

def ul(ls, **kwargs):
    return tag('ul', ''.join(map(li, ls)), **kwargs)

def label(c, **kwargs):
    return tag('label', c, **kwargs)

def img(src, **kwargs):
    return tag('img', src=src, **kwargs)

def div(c, **kwargs):
    return tag('div', c, **kwargs)

def span(c, **kwargs):
    return tag('span', c, **kwargs)

def button(c, **kwargs):
    return tag('button', c, **kwargs)

def body(c, **kwargs):
    return tag('body', c, **kwargs)

def hidden(name, value, **kwargs):
    return input('hidden', name=name, value=value, **kwargs)

def h1(c, **kwargs):
    return tag('h1', c, **kwargs)

def text(name, value='', **kwargs):
    return input('text', value=value, name=name, **kwargs)

def submit(value='Submit', name=None, **kwargs):
    return input('submit', name=name, value=value, **kwargs)

def password(**kwargs):
    return input('password', name='password', **kwargs)

def b(c):
    return tag('b', c)

def br():
    return tag('br')

def input(type, value='', name=None, **kwargs):
    return tag('input', value=value, type=type, name=name, **kwargs)

def form(c, method='post', **kwargs):
    return tag('form', c, method=method, **kwargs)

def textarea(c, rows, cols, **kwargs):
    return tag('textarea', c, rows=rows, cols=cols, **kwargs)

def tag(name_, c=None, **kwargs):
    if isinstance(c, tuple):
        kwargs.update(c[1])
        c = c[0]

    attrs = u' '.join(u'{0}="{1}"'.format(k, v) for k, v in kwargs.items() if v is not None)
    if c is None:
        return '<{} {}>'.format(name_, attrs)
    else:
        return u'<{0} {1}>{2}</{3}>'.format(name_, attrs, c, name_)
