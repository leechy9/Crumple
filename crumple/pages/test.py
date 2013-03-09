import framework.page as fp
import framework.wsgi as wsgi

def application(environ, start_response):
    template = r'template1.tmpl'
    envi = wsgi.Envi(environ, start_response, True)
    page = fp.TemplatePage(envi, template)
    return page.get_output()
