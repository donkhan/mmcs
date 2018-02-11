import xlrd
import zipfile
from CustomerOperation import *
import shutil
import auth


class Registration:

    def __init__(self):
        #self.headers = {"Api-key": auth.auth()}
        self.headers = {}

    def done(self):
        logging.debug("Going to delete %s",self.folder)
        shutil.rmtree(self.folder)
        logging.debug("Deleted %s",self.folder)


class IndividualRegistration(Registration):

    def __init__(self,t):
        self.customer_operation = CustomerOperation(t[0])
        self.folder = t[0]
        self.pay_load = t[1]
        Registration.__init__(self)

    def process(self):
        self.customer_operation.start_customer_on_boarding(self.headers,self.get_customer(self.pay_load))
        self.done()

    @staticmethod
    def get_customer(post_data):
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


class XLRegistration(Registration):

    def __init__(self,folder):
        self.customer_operation = CustomerOperation(folder)
        self.folder = folder
        Registration.__init__(self)

    @staticmethod
    def extract_images(folder):
        zip_ref = zipfile.ZipFile(folder + "/images.zip", 'r')
        zip_ref.extractall(folder)
        zip_ref.close()

    def process(self):
        self.extract_images(self.folder)
        workbook = xlrd.open_workbook(self.folder+'/temp.xlsx')
        sheet = workbook.sheet_by_index(0)
        row = 1
        while row < sheet.nrows:
            customer = self.get_customer(sheet,row)
            self.customer_operation.start_customer_on_boarding(self.headers,customer)
            row = row + 1
        self.done()

    @staticmethod
    def get_customer(sheet,row):
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


