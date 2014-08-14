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

import os
import sys

'''
This file stores variables used throughout the framework.
Meant to be edited by the user.
'''

'''
The following are for automagically finding out where the script resides.
'''
script_location = os.path.dirname(os.path.normpath(__file__))
base_location = os.path.normpath(os.path.join(script_location, '..'))

'''
Add the `library` directory to the system path.
'''
sys.path.append(os.path.join(base_location, 'libraries'))

'''
The root directory that templates are stored in. Should be automatically
configured, but available to edit as a fallback.
'''
template_location = os.path.join(base_location, 'templates')


'''
Sets the Content-Type http response header.
For most uses, this can be left alone.
Use the HTML5 header to have less strict parsing: text/html
The standard header for xhtml: application/xhtml+xml
'''
content_type = 'text/html'
#content_type = 'application/xhtml+xml'


'''
Sets the default doctype appended to the top of each page.
This value must be a byte-string for Python 2 and 3 compatibility.
The default is the XHTML5/HTML5 doctype.
'''
doctype = b'<!DOCTYPE html>\n'

'''
The standard block size to use when reading a file.
'''
block_size = 4096

