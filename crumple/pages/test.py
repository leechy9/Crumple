# This page executes the testing suite for Crumple
import framework.page as fp
import framework.wsgi as wsgi

def application(environ, start_response):
    template = r'test/tests.tmpl'
    envi = wsgi.Envi(environ, start_response, True)
    page = fp.TemplatePage(envi, template)
    return page.get_output()
