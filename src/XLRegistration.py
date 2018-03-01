from BulkRegistration import *
import xlrd


class XLRegistration(BulkRegistration):

    def __init__(self,folder):
        BulkRegistration.__init__(self,folder)


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

        front = str(sheet.cell(row,11).value)
        back = str(sheet.cell(row, 12).value)

        return {
            'idType' : doc_type,'idNo': id_no,
            'email' : email_id, 'nationality' : nationality,
            'mobile' : mobile, 'customerName' : name,
            'address' : address, 'city' : city,
            'state' : state, 'postalCode' : postal_code, 'country': nationality,
            'type' : type, 'dob' : dob, 'idExpiryDate' : '1-1-2030',
            'registeredThrough' : 'MREMIT','front_file' : front, 'back_file': back
        }
