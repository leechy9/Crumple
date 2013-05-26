# Part of the testing suite. Checks for a user input and outputs it.
import xml.etree.ElementTree as ET

def get_output(envi, insert=[]):
    user_input = envi.get_input("testType")
    span = ET.Element("span")
    span.text = str(user_input)
    return span
