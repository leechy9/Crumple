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
import os.path
import copy

# Framework imports
import framework.config as cfg
import framework.extension as ext

class TemplateParser:
    """
    A custom object used in a TreeBuilder to parse the templates.
    See the xml.etree.ElementTree for more info on TreeBuilder.
    """

    def __init__(self, envi, insert=[]):
        """
        Args:
          insert (list[Element]): the list of Elements to insert
            (default is an empty list)
        """
        self._envi = envi
        self._is_first_element = True
        self._is_tail_data = False
        self._tmp_element = None
        self._previous_element = None
        self._root_element = None
        self._insert = insert
        self._elem_stack = []


    def _replace_element(self, root_elem, find_elem, replace_elems):
        """
        Utility method used to replace an element with another element.
        Internal use only.
        Args:
           root_elem (Element): the root element to search through
           find_elem (Element): the element to find and replace
           replace_elems (list[Element]): the list of elements replacing find_elem
        """
        # Fix for deprecated method in Python versions less than 2.7
        try:
            iterator = root_elem.iter()
        except NameError:
            iterator = root_elem.getiterator()
        # Search for the elements to replace
        for elem in iterator:
            index = 0
            while index < len(elem):
                # Replace the elements
                if elem[index] == find_elem:
                    del elem[index]
                    i = 0
                    while i < len(replace_elems):
                        elem.insert(i+index, replace_elems[i])
                        i += 1
                index += 1
    

    def start(self, tag, attrib):
        """Handle the opening of tags"""
        self._is_tail_data = False
        self._tmp_element = ET.Element(tag, attrib)
        # Check to see if first element
        # If so, create root element
        # If not, append element to previous in the stack
        if self._is_first_element:
            self._is_first_element = False
            self._root_element = self._tmp_element
            self._elem_stack.append(self._tmp_element)
        else:
            self._elem_stack[-1].append(self._tmp_element)
            self._elem_stack.append(self._tmp_element)


    def end(self, tag):
        """Handle the closing of tags"""
        self._previous_element = self._elem_stack.pop()
        self._is_tail_data = True
        # Replace _template tag with parsed output
        if tag == '_template':
            # Create new template and get output as list of Elements
            children = list(self._previous_element)
            tmp_templ = Template( \
             self._previous_element.attrib['location'], self._envi, children)
            tmp_elems = [tmp_templ.get_output()]
            # Check if root element of the document is a template
            if self._root_element != self._previous_element:
                # Replace _template element with tmp_elems
                self._replace_element(\
                 self._root_element, self._previous_element, tmp_elems)
            else:
                self._root_element = tmp_elems[0]
        # Replace _extension tag with output
        elif tag == '_extension':
            # Create new extension and get output as list of Elements
            children = list(self._previous_element)
            tmp_ext = ext.Extension( \
             self._previous_element.attrib['location'], self._envi, children)
            tmp_elems = [tmp_ext.get_output()]
            # Check if root element of the document is an extension
            if self._root_element != self._previous_element:
                # Replace _extension element with tmp_elems
                self._replace_element(\
                 self._root_element, self._previous_element, tmp_elems)
            else:
                self._root_element = tmp_elem
        # Replace _insert tag with the list of elements to insert
        elif tag == '_insert':
            # Create a copy of an object so that tail data is not duplicated
            insert_copy = copy.deepcopy(self._insert)
            # Replace _insert element with the copied Element
            self._replace_element(\
             self._root_element, self._previous_element, insert_copy)
            if len(insert_copy) > 0:
                self._previous_element = insert_copy[len(insert_copy)-1]
            

    def data(self, data):
        """Handle the inner data of each tag"""
        # Check if the data is tail or inner text
        if self._is_tail_data:
            # Check if tail already exists so data can be appended properly
            if self._previous_element.tail is not None:
                self._previous_element.tail += data
            else:
                self._previous_element.tail = data
        else:
            self._elem_stack[-1].text = data

    def close(self):
        """Return the root Element"""
        return self._root_element


class Template:
    """
    A template object. Resposible for reading and parsing template files.
    """

    def __init__(self, location, envi, insert=[]):
        """
        Recursively parse this template and all sub-templates
        Args:
          location (string): relative location to import
          envi (framework.wsgi.envi): the envi object to give to the extension
          insert (list[Element]): list of Elements to replace _insert tags
            (default is an empty list)
        """
        # Get absolute path to template from relative path given
        template_loc = os.path.join(cfg.template_location, location)
        template_text = ''
        with open(template_loc) as template_file:
            for line in template_file:
                template_text += line
        # Parse the template
        target = TemplateParser(envi, insert)
        parser = ET.XMLTreeBuilder(target=target)
        parser.feed(template_text)
        self._template_root = parser.close()
        

    def get_output(self):
        """
        Returns: The parsed template as an Element
        """
        return self._template_root


