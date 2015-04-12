import os.path
import urlparse
import core

BANNERS_FILE = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'banners.csv')

# in real application file name should be get from config file
banrot = core.BanRot.from_csv(BANNERS_FILE, delimiter=';')


banner_template = '''<img alt="{url}" src="{url}" />'''

def application(environ, start_response):
    qs = urlparse.parse_qs(environ.get('QUERY_STRING', ''))
    categories = qs.get('category', [])
    banner = banrot.next_banner(categories)
    content = banner_template.format(url = banner.url)
    start_response('200 OK', [('Content-Type', 'text/html')])
    return content


if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    port = 5000
    print 'Running on http://127.0.0.1:{}/'.format(port)
    httpd = make_server('', port, application)
    httpd.serve_forever()



