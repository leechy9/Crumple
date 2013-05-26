# This is a simple example that outputs a "Hello World" paragraph.
import xml.etree.ElementTree as ET

def get_output(envi, insert=[]):
    p = ET.Element("p")
    p.text = "Hello World"
    return p
