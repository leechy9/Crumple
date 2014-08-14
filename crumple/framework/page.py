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
import os.path
import xml.etree.ElementTree as ET

# Framework Imports
import framework.template as tmpl
import framework.extension as ext
import framework.config as cfg
import framework.wsgi

class CrumplePage(object):
    '''
    An abstract page object. Defines the structure of a Page object.
    '''

    def __init__(self, location, envi):
        '''
        Create page and send response headers to client
        Args:
          location (string): location of the content to serve
          envi (framework.wsgi.envi): the envi object for this page to use
        '''
        self.location = location
        self.envi = envi
        self.output = []

    def _generate_content(self):
        '''
        To be implemented by children. Appending to self.output should be
        done here to create the content of the page.
        '''
        pass

    def get_output(self):
        '''
        Automatically calculate the Content-Length http header and start
        sending out the page.
        Returns:
          The output of the page in a list.
        '''
        length = 0
        for line in self.output:
            length += len(line)
        self.envi.extend_headers([('Content-Length', str(length))])
        self.envi.start_response()
        return self.output
    

class TemplatePage(CrumplePage):
    '''
    A web page with a template as the initial frame.
    Reads in a valid template and creates a page from it.
    '''

    def __init__(self, location, envi, doctype=None):
        '''
        Create page and prepare headers to send to the client.
        Args:
          location (string): relative location of the root template
          envi (framework.wsgi.envi): the envi object for this page to use
          doctype (string): the doctype to use for this page. 
           (default is the value set in framework.config)
        '''
        super(TemplatePage, self).__init__(location, envi)
        if doctype is None:
            self.doctype = cfg.doctype
        else:
            self.doctype = doctype
        self._generate_content()

    def _generate_content(self):
        '''
        Responsible for handling the content generated.
        Automagically find templates to use.
        '''
        self.root_template = tmpl.Template(self.location, self.envi)
        self.output.append(self.doctype)
        self.output.append(ET.tostring(self.root_template.get_output(), 'UTF-8'))
        


class ExtensionPage(CrumplePage):
    '''
    A web page with an extension as the initial frame.
    Imports a valid extension and creates a page from it.
    '''

    def __init__(self, location, envi, doctype=None):
        '''
        Create page and prepare headers to send to the client.
        Args:
          envi (framework.wsgi.envi): the envi object for this page to use
          location (string): relative location of the root extension
          doctype (string): the doctype to use for this page.
            (default is the value set in framework.config)
        '''
        super(ExtensionPage, self).__init__(location, envi)
        if doctype is None:
            self.doctype = cfg.doctype
        else:
            self.doctype = doctype
        self._generate_content()

    def _generate_content(self):
        '''
        Responsible for handling the content generated.
        Automagically find extensions to use.
        '''
        self.root_extension = ext.Extension(self.location, self.envi)
        self.output.append(self.doctype)
        self.output.append(ET.tostring(self.root_extension.get_output(), 'UTF-8'))


class StaticPage(CrumplePage):
    '''
    A web page with a static file as its content.
    '''

    def __init__(self, location, envi, file_name=None):
        '''
        Create the page and prepare the appropriate headers.
        Args:
          envi (framework.wsgi.envi): the envi object for this page to use
          location (string): relative location of the root extension
          file_name (string): the name of the file the client will receive
            (default is the base name of location)
        '''
        super(StaticPage, self).__init__(location, envi)
        if file_name is None:
            file_name = os.path.basename(location)
        file_size = os.path.getsize(location)
        envi.append_header('Content-Type', 'application/octet-stream')
        envi.append_header('Content-Length', str(file_size))
        envi.append_header(\
         'Content-Disposition', 'attachment; filename=' + file_name)
        self._generate_content()


    def get_output(self):
        '''
        Overrides the parent's method. Serves the static file through the os
        facilities to improve speed, if avaiable. If not, defaults to slower
        fallback.
        Returns:
          An iterable wrapping the file to be served.
        '''
        self.envi.start_response()
        raw_file = open(self.location, 'rb')
        if 'wsgi.file_wrapper' in self.envi.environ:
            # Let the file_wrapper callable handle the serving
            file_wrapper = self.envi.environ['wsgi.file_wrapper']
            return file_wrapper(raw_file, cfg.block_size)
        else:
            # Stop when b'' is encountered, otherwise send a block.
            return iter(lambda: raw_file.read(cfg.block_size), b'')

