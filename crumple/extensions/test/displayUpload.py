# Part of the testing suite. Checks for a file upload and outputs its file name
import xml.etree.ElementTree as ET

import framework.page as fp

def get_output(envi, insert=[]):
    uploaded_file = envi.get_file("testFile")
    span = ET.Element("span")
    if uploaded_file is not None:
        span.text = uploaded_file.filename
    else:
        span.text = "No file was uploaded"
    return span
