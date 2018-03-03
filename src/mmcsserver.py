from SocketServer import ThreadingMixIn
from BaseHTTPServer import HTTPServer
import BaseHTTPServer
import ConfigParser
import re
from Download import *
from CSVRegistration import *
from XLRegistration import *
from IndividualRegistration import *

hello_path = re.compile("^/hello$")
register_customers_path = re.compile("^/register/customers$")
register_customer_path = re.compile("^/register/customer$")


class ThreadingServer(ThreadingMixIn, HTTPServer):
    pass


class RequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):

    def send_data(self, code, content_type, data):
        self.send_response(code)
        self.send_header('Content-type', content_type)
        self.send_header("Content-Length",len(data))
        self.end_headers()
        self.wfile.write(data)

    def check_access(self):
        return self.client_address[0] == '127.0.0.1'

    def do_GET(self):
        logging.debug("Path %s", self.path)
        tokens = self.path.split('?')
        path = tokens[0]
        qs = ""
        if len(tokens) > 1:
            qs = tokens[1]
        if hello_path.match(path):
            self.send_data(httplib.OK, "text", "Hello from Customer Registration Service")
        else:
            self.send_data(httplib.NOT_FOUND, "text", self.path + " not found ")

    def do_POST(self):
        logging.debug("Path %s", self.path)
        if register_customer_path.match(self.path):
            self.send_data(httplib.OK, "json",
                json.dumps(IndividualRegistration(DownloadContent().download_all_content(self.rfile, self.headers)).process()))
        elif register_customers_path.match(self.path):
            download = Download().download_all_content(self.rfile, self.headers)
            if download[1].endswith("csv"):
                self.send_data(httplib.OK, "json", json.dumps(CSVRegistration(download[0]).process()))
            else:
                self.send_data(httplib.OK, "json", json.dumps(XLRegistration(download[0]).process()))
        else:
            self.send_response(httplib.NOT_FOUND)


config = ConfigParser.ConfigParser()
config.read("conf/application.conf")
logging.basicConfig(filename=config.get("logging","log-file"),level=logging.DEBUG)
port = config.get("networking",'web-server-port')
server_host = config.get("networking", "web-server-host")

ThreadingServer((server_host, int(port)), RequestHandler).serve_forever()
