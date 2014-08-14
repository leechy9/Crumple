# Part of the testing suite. Checks the extension insert feature.
import xml.etree.ElementTree as ET

from test_import1.test_import2.import_file2 import test_libraries

def cookies(envi, insert=[]):
    cookie = envi.get_cookie('test_cookie')
    if not cookie:
        envi.append_header('Set-Cookie', 'test_cookie=blah')
    span = ET.Element('span')
    span.text = str(cookie)
    return span

def imports(envi, insert=[]):
    p = ET.Element('p')
    p.text = 'The path '
    em = ET.SubElement(p, 'em')
    em.text = test_libraries()
    em.tail = ' was successfully imported.'
    return p

def inputs(envi, insert=[]):
    user_input = envi.get_input('testType')
    span = ET.Element('span')
    span.text = str(user_input)
    return span

def uploads(envi, insert=[]):
    uploaded_file = envi.get_file('testFile')
    span = ET.Element('span')
    if uploaded_file is not None:
        span.text = uploaded_file.filename
    else:
        span.text = 'No file was uploaded'
    return span

def test1(envi, insert=[]):
    div = ET.Element('div')
    div.extend(insert)
    return div

def test2(envi, insert=[]):
    items = ['apple', 'banana', 'turtle']
    ol = ET.Element('ol')
    for i in items:
        li = ET.SubElement(ol, 'li')
        li.text = i
    return ol
