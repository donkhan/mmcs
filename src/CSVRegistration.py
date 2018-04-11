from BulkRegistration import *


class CSVRegistration(BulkRegistration):

    def __init__(self,folder):
        BulkRegistration.__init__(self,folder)

    def process(self):
        print self.folder
        self.extract_images(self.folder)
        fd = open(self.folder+'/temp.csv')
        fd.readline()
        s = fd.readline()
        boarding_statuses = []
        while s != "" and s != '\n':
            boarding_statuses.append(self.customer_operation.start_customer_on_boarding(self.headers,self.get_customer(s)))
            s = fd.readline()
        self.done()
        return boarding_statuses

    def get_customer(self,line):
        record = line.split(",")
        email_id = record[0]
        if email_id == 'NULL':
            email_id = record[3].split()[0] + "-" + record[5] + "@maxmoney.com"
        nationality = record[1]
        mobile = '+' + record[2]
        name = record[3]
        doc_type = record[4]
        id_no = record[5]
        dob = record[6]
        address = record[7]
        city = record[8]
        state = record[9]
        postal_code = record[10]
        type = record[11]
        if doc_type == 'National IC':
            doc_type = "NRIC"
        country = record[12]
        front = record[13].replace("\r\n","")
        if len(record) > 14:
            back = record[14].replace("\r\n","")
        else:
            back = front
        front = front.replace("\n","")
        back = back.replace("\n","")
        (front,back) = self.get_file(front,back,self.folder)
        customer = {
            'idType': doc_type, 'idNo': id_no,
            'email': email_id, 'nationality': nationality,
            'mobile': mobile, 'customerName': name,
            'address': address, 'city': city,
            'state': state, 'postalCode': postal_code, 'country': country,
            'type': type, 'dob': dob, 'idExpiryDate': '1-1-3030','status' : 'Unapproved',
            'registeredThrough': 'agent', 'front' : 'image/'+front, 'back': 'image/'+back
        }
        print customer
        return customer


