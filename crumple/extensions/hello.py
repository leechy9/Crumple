import xml.etree.ElementTree as ET

def get_output(insert=[]):
    p = ET.Element("p")
    p.text = "Hello World"
    return p
