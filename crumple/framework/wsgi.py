'''
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
'''

import cgi
import os.path
import wsgiref.util
# Python 2 compatibility check
try:
    import http.cookies as cookie
except ImportError:
    import Cookie as cookie

import framework.config as cfg


class Envi:
    '''
    Handles the WSGI environ and start_response objects.
    '''

    def __init__(self, environ, start_response, use_defaults=True):
        '''
        Create a new Envi for handling WSGI objects.
        Args:
          environ: WSGI standard environ variable
          start_response: WSGI standard start_response variable
          use_defaults (boolean):
            True uses the Content-Type set in config and '200 OK' as the status.
            False requires the status and Content-type to be set manually.
        '''
        self._start_response = start_response
        self.environ = environ
        self.response_headers = []
        # Handle headers and response
        if use_defaults:
            self.status = '200 OK'
            self.response_headers.append(('Content-Type', cfg.content_type))
        else:
            self.status = ''
        # Handle cookies
        if 'HTTP_COOKIE' in self.environ:
            self.cookies = cookie.SimpleCookie(environ['HTTP_COOKIE'])
        else:
            self.cookies = cookie.SimpleCookie()
        # Handle GET and POST data
        self.field_storage = cgi.FieldStorage( \
         self.environ['wsgi.input'], \
         environ=self.environ, \
         keep_blank_values=True \
        )

    def get_cookie(self, name):
        '''
        Args:
          name (string): name of the cookie to get the value from.
        Returns: The string value of the cookie or None if it does not exist.
        '''
        try:
            return self.cookies[name].value
        except KeyError:
            return None

    def get_input(self, name):
        '''
        Checks Get and Post data for values.
        Required parameters:
          name (string): name of the input to get the value from.
        Returns: The string value of the input or None if it does not exist.
        '''
        return self.field_storage.getfirst(name)

    def get_input_list(self, name):
        '''
        Checks Get and Post data for multiple values.
        Args:
          name (string): name of the input to get the value from.
        Returns: a list[string] value of the input or an empty list if none found.
        '''
        return self.field_storage.getlist(name)

    def get_file(self, name):
        '''
        Gets the uploaded file from the name specified.
        Args:
          name (string): name of the file to retrieve.
        Returns: the file object or None if it does not exist.
         file_object.filename will get the file's name.
         file_object.file will get the stream of the file.
        '''
        # Check if the file exists
        if name in self.field_storage:
            file_object = self.field_storage[name]
            # Take only the base name of the file
            file_object.filename = os.path.basename(file_object.filename)
            # If the file does not have a name, assume it was not uploaded
            if file_object.filename == '':
                return None
            else:
                return file_object
        else:
            return None

    def append_header(self, key, value):
        '''
        Appends a single header to send to the client
        Args:
          key (string): the name of the header value that will be added
          value (string): the corresponding value to assign to the given key
        '''
        self.response_headers.append((key, value))

    def extend_headers(self, headers):
        '''
        Extends the response headers that will be sent to the client
        Args:
          headers (list[(string, string)]): list of tuples to add to the headers
        '''
        self.response_headers.extend(headers)

    def start_response(self):
        '''
        Responds to the client with the appropriate http headers
        '''
        staticmethod(self._start_response(self.status, self.response_headers))


def find_object(root, path):
    '''
    Recursively finds nested objects listed in the path. Starting at `root`.
    Each new `/` in `path` designates a new object name. Throws exceptions if
    the object cannot be found.
    Args:
      path (string): the url-style path of objects/attributes to search
    Return: the object located at the path specified
    '''
    path_split = path.split('/', 1)
    if path_split[0] == '':
        return root
    next_object = getattr(root, path_split[0])
    if len(path_split) < 2:
        path_split.append('')
    return find_object(next_object, path_split[1])

