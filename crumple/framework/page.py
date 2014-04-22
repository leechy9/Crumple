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


class TemplatePage:
    """
    A web page with a template as the initial frame.
    Reads in a valid template and creates a page from it.
    """

    def __init__(self, location, envi, doctype=None):
        """
        Create page and send response headers to client
        Args:
          location (string): relative location of the root template
          envi (framework.wsgi.envi): the envi object for this page to use
          doctype (string): the doctype to use for this page. 
           (default is the value set in framework.config)
        """
        self.envi = envi
        if doctype is None:
            self.doctype = cfg.doctype
        else:
            self.doctype = doctype
        self._root_tmpl_loc = location
        self._generate_content()
        envi.start_response()

    def _generate_content(self):
        """
        Responsible for handling the content generated.
        Automagically find extensions and templates to use.
        Set output as a string representation of xhtml.
        Set the Content-length http header.
        """
        # Generate the page
        self.root_template = tmpl.Template(self._root_tmpl_loc, self.envi)
        self.output = \
         self.doctype + \
         ET.tostring(self.root_template.get_output(), 'UTF-8')
        #Add the Content-length as an http header
        length = str(len(self.output))
        self.envi.extend_headers([('Content-length', length)])
        
    def get_output(self):
        """
        Returns: The output of the page as a list of strings.
        """
        return [self.output]


class ExtensionPage:
    """
    A web page with an extension as the initial frame.
    Imports a valid extension and creates a page from it.
    """

    def __init__(self, location, envi, doctype=None):
        """
        Create page and send response headers to client
        Args:
          envi (framework.wsgi.envi): the envi object for this page to use
          location (string): relative location of the root extension
          doctype (string): the doctype to use for this page.
            (default is the value set in framework.config)
        """
        self.envi = envi
        if doctype is None:
            self.doctype = cfg.doctype
        else:
            self.doctype = doctype
        self._root_ext_loc = location
        self._generate_content()
        envi.start_response()

    def _generate_content(self):
        """
        Responsible for handling the content generated.
        Automagically find extensions and templates to use.
        Set output as a string representation of xhtml.
        """
        # Generate the page
        self.root_extension = ext.Extension(self._root_ext_loc, self.envi)
        self.output = \
         self.doctype + \
         ET.tostring(self.root_extension.get_output(), 'UTF-8')
        #Add the Content-length as an http header
        length = str(len(self.output))
        self.envi.extend_headers([('Content-length', length)])
        
    def get_output(self):
        """
        Returns: The output of the page as a list of strings.
        """
        return [self.output]

