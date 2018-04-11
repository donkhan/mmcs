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
        boarding_statuses = []
        while row < sheet.nrows:
            boarding_statuses.append(self.customer_operation.start_customer_on_boarding(self.headers,self.get_customer(sheet,row)))
            row = row + 1
        self.done()
        return boarding_statuses

    def get_customer(self,sheet,row):
        email_id = str(sheet.cell(row, 0).value)
        if email_id == 'NULL':
            email_id = str(sheet.cell(row, 3).value).split()[0] + "-" + str(sheet.cell(row, 5).value) + "@maxmoney.com"
        nationality = str(sheet.cell(row,1).value)
        mobile = str(sheet.cell(row,2).value)
        name = str(sheet.cell(row,3).value)
        doc_type = str(sheet.cell(row,4).value)
        id_no = str(sheet.cell(row,5).value)
        dob = str(sheet.cell(row, 6).value)
        address = str(sheet.cell(row, 7).value)
        city = str(sheet.cell(row, 8).value)
        state = str(sheet.cell(row, 9).value)
        postal_code = str(sheet.cell(row, 10).value)
        type = str(sheet.cell(row,11).value)
        if doc_type == 'National IC':
            doc_type = "NRIC"
        country = str(sheet.cell(row, 12).value)
        front = str(sheet.cell(row,13).value)
        if(sheet.cell(row,14) != None):
            back = str(sheet.cell(row, 14).value)
        else:
            back = front
        (front, back) = self.get_file(front, back, self.folder)
        customer = {
            'idType': doc_type, 'idNo': id_no,
            'email': email_id, 'nationality': nationality,
            'mobile': mobile, 'customerName': name,
            'address': address, 'city': city,
            'state': state, 'postalCode': postal_code, 'country': country,
            'type': type, 'dob': dob, 'idExpiryDate': '1-1-3030', 'status': 'Unapproved',
            'registeredThrough': 'agent', 'front': 'image/' + front, 'back': 'image/' + back
        }
        return customer
