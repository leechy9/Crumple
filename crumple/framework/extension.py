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

# Standard Library Imports
import xml.etree.ElementTree as ET

# Framework imports
import extensions
from extensions import *
from framework.wsgi import find_object

class Extension:
    '''
    An Extension object. Resposible for importing and executing extensions.
    '''

    def __init__(self, location, envi, insert=[]):
        '''
        Args:
          location (string): relative location to import
          envi (framework.wsgi.envi): the envi object to give to the extension
          insert (list[Element]): the list of Elements to insert
            (default is an empty list)
        '''
        self._insert = insert
        self._envi = envi
        self.extension = find_object(extensions, location)

    def get_output(self):
        '''
        Returns:
          The output of the Extension as an Element.
        '''
        return self.extension(self._envi, self._insert)

