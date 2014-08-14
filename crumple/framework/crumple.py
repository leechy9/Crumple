from framework.wsgi import find_object
import pages
from pages import *

def application(environ, start_response):
    '''
    Find objects in the `pages` directory that correspond to the url after
    removing the left-most slash. Serve the appropriate content.
    '''
    try:
        found_object = find_object(pages, environ.get('PATH_INFO', '')[1:])
        response_body = found_object(environ, start_response)
    except (AssertionError, AttributeError, TypeError):
        start_response('404 Not Found', [('content-type', 'text/plain')])
        response_body = [b'The page you requested does not exist.']
    return response_body
