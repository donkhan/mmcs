from SocketServer import ThreadingMixIn
from BaseHTTPServer import HTTPServer
import BaseHTTPServer
import ConfigParser
import re
import logging
import shutil
import httplib
import cgi
import xlrd
import zipfile
import auth
import c
import requests

hello_path = re.compile("^/hello$")
register_customers_path = re.compile("^/register/customers$")

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
        if register_customers_path.match(self.path):
            form = cgi.FieldStorage(
                fp=self.rfile,
                headers=self.headers,
                environ={
                    "REQUEST_METHOD": "POST",
                    "CONTENT_TYPE": self.headers['Content-Type']
                })

            fdst = open("/tmp/temp.xlsx", "wb")
            shutil.copyfileobj(form["file"].file, fdst)
            fdst.close()

            fdst = open("/tmp/images.zip", "wb")
            shutil.copyfileobj(form["images"].file, fdst)
            fdst.close()

            self.extract_images()
            self.process_file()
            self.send_data(httplib.OK, "text", "File is Processed")
        else:
            self.send_response(httplib.NOT_FOUND)

    def do_PUT(self):
        pass

    def extract_images(self):
        zip_ref = zipfile.ZipFile("/tmp/images.zip", 'r')
        zip_ref.extractall("/tmp")
        zip_ref.close()

    def process_file(self):
        #headers = {"Api-key": auth.auth()}
        workbook = xlrd.open_workbook('/tmp/temp.xlsx')
        sheet = workbook.sheet_by_index(0)
        row = 0
        while row < sheet.nrows:
            customer = self.get_customer(sheet,row)
            print customer
            self.start_customer_on_boarding({},customer)
            row = row + 1

    def get_customer(self,sheet,row):
        doc_type = str(sheet.cell(row, 0).value)
        id_no = str(sheet.cell(row,1).value)
        email_id = str(sheet.cell(row,2).value)
        nationality = str(sheet.cell(row,3).value)
        mobile = str(sheet.cell(row,4).value)
        name = str(sheet.cell(row,5).value)
        dob = str(sheet.cell(row,6).value)
        address = str(sheet.cell(row,6).value)
        city = str(sheet.cell(row, 7).value)
        state = str(sheet.cell(row, 8).value)
        postal_code = str(sheet.cell(row, 9).value)
        type = str(sheet.cell(row,10).value)
        print(doc_type)
        if doc_type == 'NRIC':
            id_no = '930830135870'
        dob = "1-1-2000"
        type = 'Individual'
        state = 'KUALA_LUMPUR'
        mobile = '+63123451942'
        return {
            'idType' : doc_type,'idNo': id_no,
            'email' : email_id, 'nationality' : nationality,
            'mobile' : mobile, 'customerName' : name,
            'address' : address, 'city' : city,
            'state' : state, 'postalCode' : postal_code, 'country': nationality,
            'type' : type, 'dob' : dob, 'idExpiryDate' : '1-1-2030',
            'registeredThrough' : 'MREMIT'
        }

    def get_files(self,customer):
        print "File Name " + customer['idNo'] + '_F'
        front = open('/tmp/'+customer['idNo'] + '_F.png')
        back = open('/tmp/' + customer['idNo'] + '_B.png')
        files = {
            'front': front, 'back': back
        }
        return files

    def start_customer_on_boarding(self,headers,customer):
        self.register_customer(headers,customer,[self.update_images,self.approve_customer,
                                                 self.convert_customer])

    def register_customer(self,headers,customer,next_functions):
        logging.debug("Registering Customer %s ", customer.get('customerName'))
        url = "/customers"
        response = requests.post(c.site + url, verify=False, headers=headers, data=customer)
        status_code = response.status_code
        logging.debug("Registration Status Code %d",status_code)
        if status_code >= 200 and status_code < 300:
            next_functions[0](headers,customer,next_functions[1:])

    def update_images(self,headers,customer,next_functions):
        logging.debug("Updating images of " + customer.get('customerName'))
        url = "/customers/" + customer['idNo']
        response = requests.put(c.site + url, verify=False, headers=headers, data=customer,files=self.get_files(customer))
        status_code = response.status_code
        logging.debug("Updating Status Code %d", status_code)
        if status_code == 200:
            next_functions[0](headers, customer, next_functions[1:])

    def approve_customer(self,headers,customer,next_functions):
        logging.debug("Approve " + customer.get('customerName'))
        url = "/customers/" + customer['idNo'] + "/approve"
        response = requests.post(c.site + url, verify=False, headers=headers, data={})
        status_code = response.status_code
        logging.debug("Approval Status Code %d", status_code)
        if status_code == 204:
            next_functions[0](headers, customer, next_functions[1:])

    def validate_customer(self,headers,customer,next_functions):
        logging.debug("Validating Customer %s",customer.get('customerName'))
        url = "/customers/" + customer['idNo'] + "/validate"
        response = requests.put(c.site + url, verify=False, headers=headers, data={})
        status_code = response.status_code
        logging.debug("Validating Status Code %d", status_code)
        if status_code == 200:
            next_functions[0](headers, customer, next_functions[1:])

    def convert_customer(self, headers, customer, next_functions):
        logging.debug("Converting Customer %s", customer.get('customerName'))
        url = "/customers/" + customer['idNo'] + "/convert-by-agent"
        response = requests.post(c.site + url, verify=False, headers=headers, data={})
        status_code = response.status_code
        logging.debug("Converting Status Code %d", status_code)


logging.basicConfig(filename='/tmp/mmcs.log',level=logging.DEBUG)

config = ConfigParser.ConfigParser()
config.read("conf/application.conf")
port = config.get("networking",'web-server-port')
server_host = config.get("networking", "web-server-host")

ThreadingServer((server_host, int(port)), RequestHandler).serve_forever()
