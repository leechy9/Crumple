# This is a simple example that outputs a "Hello World" paragraph.
import xml.etree.ElementTree as ET

def hello(envi, insert=[]):
    p = ET.Element("p")
    p.text = "Hello World"
    return p

def print_environ(envi, insert):
    html = ET.Element('html')
    head = ET.SubElement(html, 'head')
    body = ET.SubElement(html, 'body')
    title = ET.SubElement(head, 'title')
    title.text = 'Extension Test'
    h1 = ET.SubElement(body, 'h1')
    h1.text = 'Extension Test'
    p = ET.SubElement(body, 'p')
    p.text = 'This is the environment data received from the server.'
    p = ET.SubElement(body, 'p')
    p.text = str(envi.environ)
    return html
