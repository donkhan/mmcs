from BulkRegistration import *


class CSVRegistration(BulkRegistration):

    def __init__(self,folder):
        BulkRegistration.__init__(self,folder)

    def process(self):
        self.extract_images(self.folder)
        fd = open(self.folder+'/temp.csv')
        fd.readline()
        s = fd.readline()

        while s != "":
            customer = self.get_customer(s)
            self.customer_operation.start_customer_on_boarding(self.headers,customer)
            s = fd.readline()
        self.done()

    @staticmethod
    def get_customer(line):
        record = line.split(",")
        print record
        email_id = record[0]
        if email_id == 'NULL':
            email_id = record[3].split()[0] + "-" + record[2] + "@maxmoney.com"

        doc_type = record[4]
        id_no = record[5]
        nationality = record[1]
        name = record[3]
        address = record[7]
        city = record[9]
        postal_code = record[10]
        mobile = record[2]
        state = record[9]
        dob = record[6]
        type = record[11]
        if doc_type == 'National IC':
            doc_type = "NRIC"
        dob = "1-1-2000"

        front = record[12]
        if len(record) > 12:
            back = record[13]
        else:
            back = front
        return {
            'idType': doc_type, 'idNo': id_no,
            'email': email_id, 'nationality': nationality,
            'mobile': mobile, 'customerName': name,
            'address': address, 'city': city,
            'state': state, 'postalCode': postal_code, 'country': nationality,
            'type': type, 'dob': dob, 'idExpiryDate': '1-1-2030',
            'registeredThrough': 'MREMIT', 'front_file' : front, 'back_file': back
        }

