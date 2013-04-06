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



"""
 Stores variables used throughout the framework.
 Meant to be edited by the user.
"""


"""
 The root directory that templates are stored in. Sub-directories are
  denoted by '/'.
"""
template_location = '/srv/http/crumple/templates'


"""
 The location relative to the WSGIPythonPath to import extensions from.
 Should use '.' instead of '/' to specify sub-directories.
  (like importing packages and modules in python)
"""
extension_location = 'extensions'


"""
 Sets the Content-type http response header.
 For most uses, this can be left alone.
 The default is the standard header for xhtml: application/xhtml+xml
 Use the HTML5 header to have less strict parsing: text/html
"""
content_type = 'text/html'
#content_type = 'application/xhtml+xml'


"""
 Sets the default doctype appended to the top of each page.
 The default is the XHTML5/HTML5 doctype.
"""
doctype = '<!DOCTYPE html>\n'


"""
 Sets the maximum content-length that is allowed to be read in.
 Will throw an exception if this maximum size of a request is exceeded.
 This will need to be changed if large uploads are expected.
 The value is the number of bytes to accept before rejecting more content.
"""
# The default value is 20971520 bytes (20MB)
max_content_length = 20971520

