import xml.etree.ElementTree as ET

import framework.page as fp

def get_output(insert=[]):
    user_input = fp.envi.get_input("testType")
    span = ET.Element("span")
    span.text = str(user_input)
    return span
