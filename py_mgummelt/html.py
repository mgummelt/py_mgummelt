from urlparse import urlparse
import html_tags as tags
from html_tags import *

def script(src):
    return tags.script('', src=src)

def select(name, options):
    return tags.select(''.join(option(opt, value=opt) for opt in options),
                       name=name)

def a(href, text=None, **kwargs):
    return tags.a(text if text is not None else href, href=href, **kwargs)

def table(rows, **kwargs):
    def td(cell):
        if hasattr(cell, '__iter__'):
            return tags.td(cell[0], **cell[1])
        else:
            return tags.td(cell)
    def tr(row):
        if len(row) == 2 and isinstance(row[1], dict):
            return tags.tr(''.join(map(td, row[0])), **row[1])
        else:
            return tags.tr(''.join(map(td, row)))

    return tags.table(''.join(map(tr, rows)), **kwargs)

def ul(ls, **kwargs):
    return tags.ul(''.join(map(li, ls)), **kwargs)

def img(src, **kwargs):
    return tags.img(src=src, **kwargs)

def input(type, value='', name=None, **kwargs):
    return tags.input(value=value, type=type, name=name, **kwargs)

def hidden(name, value, **kwargs):
    return input('hidden', name=name, value=value, **kwargs)

def text(name, value='', **kwargs):
    return input('text', value=value, name=name, **kwargs)

def submit(value='Submit', name=None, **kwargs):
    return input('submit', name=name, value=value, **kwargs)

def password(**kwargs):
    return input('password', name='password', **kwargs)

def form(c, method='post', **kwargs):
    return tags.form(c, method=method, **kwargs)

def textarea(c, rows, cols, **kwargs):
    return tags.textarea(c, rows=rows, cols=cols, **kwargs)

def page(title_, c, css=[], js=[], less=[]):
    def css_link(href):
        return link(rel='stylesheet',
                    type='text/css',
                    href=href)

    return '<!DOCTYPE html>' + html(head(title(title_) +
                                         meta(charset='utf8') +
                                         ''.join(map(css_link, css)) +
                                         ''.join(map(script, js))) +
                                    body(c), lang='en')
