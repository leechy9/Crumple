# Part of the testing suite. Checks the extension insert feature.
import xml.etree.ElementTree as ET

def get_output(envi, insert=[]):
    div = ET.Element("div")
    div.extend(insert)
    return div
