import logging
import xlrd
import zipfile
from CustomerOperation import *
import json
import shutil

class IndividualRegistration:

    def __init__(self,folder):
        self.customer_operation = CustomerOperation(folder)
        self.folder = folder

    def process(self):
        self.customer_operation.start_customer_on_boarding({},self.get_customer())
        shutil.rmtree(self.folder)

    def get_customer(self):
        post_data = json.loads(open(self.folder + "/content.json").read())
        return {
            'idType': post_data.get('doc_type'), 'idNo': post_data.get('id_no'),
            'email': post_data.get('email_id'), 'nationality': post_data.get('nationality'),
            'mobile': post_data.get('mobile'), 'customerName': post_data.get('name'),
            'address': post_data.get('address'), 'city': post_data.get('city'),
            'state': post_data.get('state'), 'postalCode': post_data.get('postal_code'), 'country': post_data.get('nationality'),
            'type': type, 'dob': post_data.get('dob'), 'idExpiryDate': '1-1-2030',
            'registeredThrough': 'MREMIT'
        }
        return customer


class XLRegistration:
    def __init__(self,folder):
        self.customer_operation = CustomerOperation(folder)
        self.folder = folder

    def extract_images(self):
        zip_ref = zipfile.ZipFile(self.folder + "/images.zip", 'r')
        zip_ref.extractall(self.folder)
        zip_ref.close()

    def process(self):
        #headers = {"Api-key": auth.auth()}
        self.extract_images()
        workbook = xlrd.open_workbook(self.folder+'/temp.xlsx')
        sheet = workbook.sheet_by_index(0)
        row = 0
        while row < sheet.nrows:
            customer = self.get_customer(sheet,row)
            self.customer_operation.start_customer_on_boarding({},customer)
            row = row + 1
        shutil.rmtree(self.folder)
        
    def get_customer(self,sheet,row):
        doc_type = str(sheet.cell(row, 0).value)
        id_no = str(sheet.cell(row,1).value)
        email_id = str(sheet.cell(row,2).value)
        nationality = str(sheet.cell(row,3).value)
        name = str(sheet.cell(row,5).value)
        address = str(sheet.cell(row,6).value)
        city = str(sheet.cell(row, 7).value)
        postal_code = str(sheet.cell(row, 9).value)
        mobile = str(sheet.cell(row, 4).value)
        state = str(sheet.cell(row, 8).value)
        dob = str(sheet.cell(row, 6).value)
        type = str(sheet.cell(row,10).value)
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


