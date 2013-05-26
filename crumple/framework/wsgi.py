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
import tempfile
import os.path
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

        # Deny extremely large requests immediately
        content_length = int(self.environ.get('CONTENT_LENGTH', '0'))
        if content_length > cfg.max_content_length:
            raise Exception('Maximum Content-length exceeded.')

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
        
        # Read the content into a temporary file
        input_stream = self.environ['wsgi.input']
        temp_file = tempfile.TemporaryFile(mode='w+b')
        total_length = 0
        # Keep reading bytes until the content length is reached
        while content_length > 0:
            # Get the amount of data to read from the stream 200KB chunks
            chunk_size = min(content_length, 204800)
            chunk = input_stream.read(chunk_size)
            # Stop if attempting to read non-existent bytes
            if not chunk:
                break
            # Check to ensure extremely large content is not accepted.
            total_length += len(chunk)
            if total_length > cfg.max_content_length:
                raise Exception('Maximum Content-length exceeded.')
            # Write stream to temporary file
            temp_file.write(chunk)
            content_length -= len(chunk)
        # Allow the input to be read again later
        temp_file.seek(0)
        self.environ['wsgi.input'] = temp_file

        # Handle GET and POST data with the temporary file of inputs
        self.field_storage = cgi.FieldStorage( \
         temp_file, \
         environ=self.environ, \
         keep_blank_values=True \
        )

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
     Checks Get and Post data for multiple values.
     Returns a list(string) value of the input or an empty list if none found.
     Required parameters:
       name - string, name of the input to get the value from.
    """
    def get_input_list(self, name):
        return self.field_storage.getlist(name)

    """
     Gets the uploaded file from the name specified.
     Returns the file object or None if it does not exist.
      Accessing the returned file_object.filename will get the file's name.
      Accessing the returned file_object.file will get the stream of the file.
     Required parameters:
       name - string, name of the file to retrieve.
    """
    def get_file(self, name):
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


