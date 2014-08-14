import os.path

import framework.page as fp
import framework.wsgi as wsgi
import framework.config as cfg

def full_test(environ, start_response):
    '''
    Tests all possible scenarios in Crumple.
    '''
    template = r'test/tests.tmpl'
    envi = wsgi.Envi(environ, start_response, True)
    page = fp.TemplatePage(template, envi)
    return page.get_output()

def extension_page(environ, start_response):
    '''
    An example of an extension page that displays the WSGI environ object.
    '''
    extension = r'simple/print_environ'
    envi = wsgi.Envi(environ, start_response, False)
    envi.status = '200 OK'
    envi.extend_headers([('Content-Type', 'text/html')])
    page = fp.ExtensionPage(extension, envi)
    return page.get_output()

def template_page(environ, start_response):
    '''
    A simple example of a template page.
    '''
    template = r'template1.tmpl'
    envi = wsgi.Envi(environ, start_response, True)
    page = fp.TemplatePage(template, envi)
    return page.get_output()

def static_page(environ, start_response):
    '''
    A simple example of a static page.
    '''
    static_location = \
     os.path.join(cfg.base_location, 'templates/test/tests.tmpl')
    envi = wsgi.Envi(environ, start_response, False)
    envi.status = '200 OK'
    page = fp.StaticPage(static_location, envi, 'StaticFile.txt')
    return page.get_output()

