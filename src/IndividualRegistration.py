from CustomerOperation import *
from Registration import *


class IndividualRegistration(Registration):

    def __init__(self,t):
        self.customer_operation = CustomerOperation(t[0])
        self.folder = t[0]
        self.pay_load = t[1]
        Registration.__init__(self)

    def process(self):
        customer = self.get_customer(self.pay_load)
        on_boarding_status = self.customer_operation.start_customer_on_boarding(self.headers,customer)
        self.done()
        return on_boarding_status

    @staticmethod
    def get_customer(post_data):
        front = str(post_data.get('id_no'))+"_F.png"
        back = str(post_data.get('id_no'))+"_B.png"
        return {
            'idType': post_data.get('doc_type'), 'idNo': post_data.get('id_no'),
            'email': post_data.get('email_id'), 'nationality': post_data.get('nationality'),
            'mobile': post_data.get('mobile'), 'customerName': post_data.get('name'),
            'address': post_data.get('address'), 'city': post_data.get('city'),
            'state': post_data.get('state'), 'postalCode': post_data.get('postal_code'), 'country': post_data.get('nationality'),
            'type': type, 'dob': post_data.get('dob'), 'idExpiryDate': '1-1-2030',
            'registeredThrough': 'agent', 'front_file' : front, 'back_file' : back, type : 'Individual'
        }
        return customer