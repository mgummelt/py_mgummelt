from urlparse import urlparse, parse_qsl, urlunparse
from urllib import urlencode

from werkzeug.serving import run_simple
from werkzeug.wrappers import Request, Response
from werkzeug.wsgi import SharedDataMiddleware
from werkzeug.datastructures import ImmutableMultiDict

class SafeRequest(Request):
    class SafeArgDict(ImmutableMultiDict):
        def __getitem__(self, k):
            v = super(ImmutableMultiDict, self).__getitem__(k) \
                                               .replace('&', '&amp;')

            syntax_chars = {'<': '&lt;',
                            '>': '&gt;',
                            '"': '&quot;',
                            "'": '&#x27;'}
            for c, r in syntax_chars.iteritems():
                v = v.replace(c, r)
            return v

    parameter_storage_class = SafeArgDict

def url_params(url, *args, **kwargs):
    ''' url with added k=v param '''
    parts = list(urlparse(url))
    query = dict(parse_qsl(parts[4]))
    query.update(kwargs)
    parts[4] = urlencode(query)
    if args:
        parts[4] += '&' + '&'.join(args)
    return urlunparse(parts)

def wsgi_app(app):
    def wsgi_app(environ, start_response):
        def start(code, headers):
            codes = {200: 'OK',
                     301: 'Moved Permanently',
                     302: 'Found',
                     404: 'Not Found'}
            return start_response('{} {}'.format(code, codes[code]), headers)

        resp = app(SafeRequest(environ))

        if isinstance(resp, Response):
            return resp(environ, start_response)
        elif isinstance(resp, basestring):
            code, body, headers = 200, resp, []
        elif isinstance(resp, int):
            code, body, headers = resp, '', []
        elif isinstance(resp, tuple):
            if len(resp) == 2:
                if type(resp[0]) is int:
                    code, headers, body = resp[0], resp[1], []
                else:
                    code, headers, body = 200, resp[0], resp[1]
            else:
                code, headers, body = resp
        else:
            raise Exception

        start(code, headers)
        return [body.encode('utf8')]

    return wsgi_app
