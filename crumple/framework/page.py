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

# Framework Imports
import framework.template as tmpl
import framework.extension as ext
import framework.config as cfg
import framework.wsgi


"""
 A web page with a template as the initial frame.
 Reads in a valid template and creates a page from it.
"""
class TemplatePage:

    """
     Create page and send response headers to client
     Required parameters:
       envi - framework.wsgi.envi, the envi object for this page to use
       location - string, location of the root template
    """
    def __init__(self, envi, location):
        _set_envi(envi)
        self.envi = envi
        self.doctype = cfg.doctype
        self._root_tmpl_loc = location
        self._generate_content()
        envi.start_response()

    """
     Responsible for handling the content generated.
     Automagically find extensions and templates to use.
     Set output as a string representation of xhtml.
     Set the Content-length http header.
    """
    def _generate_content(self):
        # Generate the page
        self.root_template = tmpl.Template(self._root_tmpl_loc)
        self.output = \
         self.doctype + \
         ET.tostring(self.root_template.get_output(), 'utf-8')
        #Add the Content-length as an http header
        length = str(len(self.output))
        self.envi.extend_headers([('Content-length', length)])
        
    """
     Return the output of the page as a list of strings.
    """
    def get_output(self):
        return [self.output]


"""
 A web page with an extension as the initial frame.
 Imports a valid extension and creates a page from it.
"""
class ExtensionPage:

    """
     Create page and send response headers to client
     Required parameters:
       envi - framework.wsgi.envi, the envi object for this page to use
       location - string location of the root extension
    """
    def __init__(self, envi, location):
        _set_envi(envi)
        self.envi = envi
        self.doctype = cfg.doctype
        self._root_ext_loc = location
        self._generate_content()
        envi.start_response()

    """
     Responsible for handling the content generated.
     Automagically find extensions and templates to use.
     Set output as a string representation of xhtml.
    """
    def _generate_content(self):
        # Generate the page
        self.root_extension = ext.Extension(self._root_ext_loc)
        self.output = \
         self.doctype + \
         ET.tostring(self.root_extension.get_output(), 'utf-8')
        #Add the Content-length as an http header
        length = str(len(self.output))
        self.envi.extend_headers([('Content-length', length)])
        
    """
     Return the output of the page as a list of strings.
    """
    def get_output(self):
        return [self.output]



"""
 Sets envi as a global object of the page module. Internal use only.
 Required parameters:
   envi_ - envi, the object to set as the global variable named 'envi'
"""
def _set_envi(envi_):
    global envi
    envi = envi_

