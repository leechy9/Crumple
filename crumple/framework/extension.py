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

# Standard Library Imports
import xml.etree.ElementTree as ET

# Framework imports
import framework.config as cfg

"""
 An Extension object. Resposible for importing and executing extensions.
"""
class Extension:

    """
     Required parameters:
       location - String, relative location to import
       envi - framework.wsgi.envi, the envi object to give to the extension
     Optional parameters:
       insert - list(Element), the list of Elements to insert
    """
    def __init__(self, location, envi, insert=[]):
        self._insert = insert
        self._envi = envi
        # Import module from location specified
        self._extension_loc = cfg.extension_location + '.' + location
        self.module = \
         __import__(self._extension_loc, fromlist=[cfg.extension_location])

    """
     Return the output of the Extension as an Element
    """
    def get_output(self):
        # Execute the get_output() method from the extension
        return self.module.get_output(self._envi, self._insert)
