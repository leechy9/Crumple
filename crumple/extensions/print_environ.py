# This is an example of an extension that prints out the WSGI environ object.

import xml.etree.ElementTree as ET

import framework.wsgi
import framework.page


def get_output(insert):
    html = ET.Element('html')
    head = ET.SubElement(html, 'head')
    body = ET.SubElement(html, 'body')
    title = ET.SubElement(head, 'title')
    title.text = 'Extension Test'
    h1 = ET.SubElement(body, 'h1')
    h1.text = 'Extension Test'
    p = ET.SubElement(body, 'p')
    p.text = str(framework.page.envi.environ)
    return html
