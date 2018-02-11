import logging
import requests
import c


class CustomerOperation:

    def __init__(self,uuid):
        self.folder = uuid

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

    def get_files(self,customer):
        front = open(self.folder + "/"+customer['idNo'] + '_F.png')
        back = open(self.folder + "/" + customer['idNo'] + '_B.png')
        files = {
            'front': front, 'back': back
        }
        return files