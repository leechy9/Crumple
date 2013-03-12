# Part of the testing suit. Checks the extension insert feature.
import xml.etree.ElementTree as ET

def get_output(insert=[]):
    div = ET.Element("div")
    div.extend(insert)
    return div
