# -*- coding: utf-8 -*-

"""
Simple HTTP server so we are able to show Maps in browser.

"""

import sys
if sys.version_info[0] >= 3:
    from http.server import BaseHTTPRequestHandler, HTTPServer
else:
    from SimpleHTTPServer import SimpleHTTPRequestHandler as BaseHTTPRequestHandler
    from SocketServer import TCPServer as HTTPServer

import webbrowser
from textwrap import dedent


# Based on https://stackoverflow.com/a/38945907/3494126
class TemporaryHTTPServer:
    """
    A simple, temporary http web server on the pure Python 3.

    Parameters
    ----------
    host: str
        Local address on which the page will be hosted, default is '127.0.0.1'
    port: int
        Corresponding port, default 7000
    """
    def __init__(self, host=None, port=None):
        self.host = host or '127.0.0.1'
        self.port = port or 7000

        self.server_address = '{host}:{port}'.format(host=self.host, port=self.port)
        self.full_server_address = 'http://' + self.server_address

    def serve(self, html_data):
        """
        Serve html content in a suitable for us manner: allow to gracefully exit using ctrl+c and re-serve some other
        content on the same host:port

        """

        # we need a request handler with a method `do_GET` which somehow is not provided in the baseline
        class HTTPServerRequestHandler(BaseHTTPRequestHandler):
            """
            An handler of requests for the server, hosting HTML-pages.
            """

            def do_GET(self):
                """Handle GET requests"""

                # response from page
                self.send_response(200)

                # set up headers for pages
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                # writing data on a page
                if sys.version_info[0] >= 3:
                    self.wfile.write(bytes(html_data, encoding='utf'))
                else:
                    self.wfile.write(bytes(html_data))

                return

        # create a temporary server
        HTTPServer.allow_reuse_address = True
        httpd = HTTPServer((self.host, self.port), HTTPServerRequestHandler)

        # run the temporary http server with graceful exit option
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print('\n Closing the server.')
            httpd.server_close()
        except Exception:
            raise

    def open_html_in_browser(self, html_data=None):
        """
        Opens a browser window showing the html content

        Parameters
        ----------
        html_data: str
            Should be a valid html code

        Examples
        --------
        
        html_data = '''
            <!DOCTYPE html>
            <html>
            <head>
            <title> Test Page </title>
            </head>
            <body>
            <p> Seems to be working. Now give the function `open_html_in_browser` some content! </p>
            </body>
            </html>
        '''

        srvr = TemporaryHTTPServer()
        srvr.open_html_in_browser(html_data)

        """

        # open the URL in a browser (if possible, in a new window)
        webbrowser.open(self.full_server_address, new=2)

        # print a user-friendly message
        msg = '''
            Your map is available at {link}. 
            It should have been opened in your browser automatically.
            Press ctrl+c to return.
        '''.format(link=self.full_server_address)
        print(dedent(msg))

        # run server (this blocks the console!)
        self.serve(html_data)
