# Part of the testing suite. Outputs an ordered list of objects.
import xml.etree.ElementTree as ET

def get_output(envi, insert=[]):
    items = ['apple', 'banana', 'turtle']
    ol = ET.Element("ol")
    for i in items:
        li = ET.SubElement(ol, "li")
        li.text = i
    return ol
