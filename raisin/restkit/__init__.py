"""Request RESTful resources with restkit"""

from restkit import request
from restkit.errors import ResourceNotFound
from restkit.errors import Unauthorized
from restkit.errors import RequestFailed
from restkit.errors import RedirectLimit
from restkit.errors import RequestError
from restkit.errors import InvalidUrl
from restkit.errors import ResponseError
from restkit.errors import ProxyError
from restkit.errors import BadStatusLine
from restkit.errors import ParserError
from restkit.errors import UnexpectedEOF

#restkit.set_logging('debug')


def get_resource(path, content_type=None):
    """Get RESTful resource while nicely handling restkit exceptions"""
    print path, content_type
    if " " in path:
        raise AttributeError
    if content_type:
        headers = {'Accept': content_type}
    else:
        headers = {}
    try:
        res = request(path, headers=headers)
    except (ResourceNotFound,
           Unauthorized,
           RequestFailed,
           RedirectLimit,
           RequestError,
           InvalidUrl,
           ResponseError,
           ProxyError,
           BadStatusLine,
           ParserError,
           UnexpectedEOF):
        print path
        return None
    except:
        raise
    if res is None:
        return None
    body = None
    if res.status == '200 OK':
        body = res.body_string()
        if 'Content-Length' in res.headers:
            content_length = res.headers['Content-Length']
        elif 'content-length' in res.headers:
            content_length = res.headers['content-length']
        else:
            print "Warning: Content length header not found!"
            raise AttributeError
        if not len(body) == int(content_length):
            print "Warning: Body length not correct!"
            raise AttributeError
    return body
