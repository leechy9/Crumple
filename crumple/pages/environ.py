# This is an example of an extension page that displays the WSGI envrion object

import framework.page as fp
import framework.wsgi as wsgi

def application(environ, start_response):
    extension = r'print_environ'
    envi = wsgi.Envi(environ, start_response, False)
    envi.status = '200 OK'
    envi.extend_headers([('Content-type', 'text/html')])
    page = fp.ExtensionPage(envi, extension)
    return page.get_output()
