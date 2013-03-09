"""
This file is part of Crumple.

Crumple is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Crumple is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Crumple.  If not, see <http://www.gnu.org/licenses/>.
"""

import cgi
# Python 2 compatibility check
try:
    import http.cookies as cookie
except ImportError:
    import Cookie as cookie

import framework.config as cfg


"""
 Handles the WSGI environ and start_response objects.
"""
class Envi:

    """
     Create a new Envi for handling WSGI objects.
     Required parameters:
       environ - WSGI standard environ variable
       start_response - WSGI standard start_response variable
     Optional parameters:
       defaults - boolean 
         True uses the Content-type set in config and '200 OK' as the status.
         False requires the status and Content-type to be set manually.
    """
    def __init__(self, environ, start_response, defaults=False):
        self._start_response = staticmethod(start_response)
        self.environ = environ
        # Handle headers and response
        if not defaults:
            self.status = ''
            self.response_headers = []
        else:
            self.status = '200 OK'
            self.response_headers = [('Content-type', cfg.content_type)]
        # Handle cookies
        self.cookies = {}
        if 'HTTP_COOKIE' in self.environ:
            self.cookies = cookie.SimpleCookie(environ['HTTP_COOKIE'])
        # Handle GET and POST data
        self.field_storage = \
         cgi.FieldStorage(self.environ['wsgi.input'], environ=self.environ)

    """
     Returns the string value of the cookie or None if it does not exist.
     Required parameters:
       name - string, name of the cookie to get the value from.
    """
    def get_cookie(self, name):
        value = None
        if name in self.cookies:
            value = self.cookies[name].value
        return value

    """
     Checks Get and Post data for values.
     Returns the string value of the input or None if it does not exist.
     Required parameters:
       name - string, name of the input to get the value from.
    """
    def get_input(self, name):
        return self.field_storage.getfirst(name)

    """
     Extends the response headers that will be sent to the client
     Required parameters:
       headers - list((string, string)), list of tuples to add to the headers
    """
    def extend_headers(self, headers):
        self.response_headers.extend(headers)

    """
     Responds to the client with the appropriate http headers
    """
    def start_response(self):
        self._start_response.__func__(self.status, self.response_headers)


