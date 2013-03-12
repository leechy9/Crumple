import xml.etree.ElementTree as ET

def get_output(insert=[]):
    items = ['apple', 'banana', 'turtle']
    ol = ET.Element("ol")
    for i in items:
        li = ET.SubElement(ol, "li")
        li.text = i
    return ol
