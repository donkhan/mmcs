import logging
import requests
import c


class CustomerOperation:

    def __init__(self,uuid):
        self.folder = uuid

    def start_customer_on_boarding(self,headers,customer):
        self.start_chaining(headers,customer,self.get_files(customer,self.folder),
                            [self.register_customer,self.update_images,self.approve_customer,
                             self.convert_customer])

    @staticmethod
    def start_chaining(headers, customer, files,next_functions):
        next_functions[0](headers,customer,files,next_functions[1:])

    @staticmethod
    def register_customer(headers,customer,files,next_functions):
        logging.debug("Registering Customer %s ", customer.get('customerName'))
        url = "/customers"
        response = requests.post(c.site + url, verify=False, headers=headers, data=customer)
        status_code = response.status_code
        logging.debug("Registration Status Code %d",status_code)
        if status_code >= 200 and status_code < 300:
            next_functions[0](headers,customer,files,next_functions[1:])

    @staticmethod
    def update_images(headers,customer,files,next_functions):
        logging.debug("Updating images of " + customer.get('customerName'))
        url = "/customers/" + customer['idNo']
        response = requests.put(c.site + url, verify=False, headers=headers, data=customer,files=files)
        status_code = response.status_code
        logging.debug("Updating Status Code %d", status_code)
        if status_code == 200:
            next_functions[0](headers, customer,files, next_functions[1:])

    @staticmethod
    def approve_customer(headers,customer,files,next_functions):
        logging.debug("Approve " + customer.get('customerName'))
        url = "/customers/" + customer['idNo'] + "/approve"
        response = requests.post(c.site + url, verify=False, headers=headers, data={})
        status_code = response.status_code
        logging.debug("Approval Status Code %d", status_code)
        if status_code == 204:
            next_functions[0](headers, customer, files,next_functions[1:])

    @staticmethod
    def validate_customer(headers,customer,files,next_functions):
        logging.debug("Validating Customer %s",customer.get('customerName'))
        url = "/customers/" + customer['idNo'] + "/validate"
        response = requests.put(c.site + url, verify=False, headers=headers, data={})
        status_code = response.status_code
        logging.debug("Validating Status Code %d", status_code)
        if status_code == 200:
            next_functions[0](headers, customer,files, next_functions[1:])

    @staticmethod
    def convert_customer(headers, customer, files,next_functions):
        logging.debug("Converting Customer %s", customer.get('customerName'))
        url = "/customers/" + customer['idNo'] + "/convert-by-agent"
        response = requests.post(c.site + url, verify=False, headers=headers, data={})
        status_code = response.status_code
        logging.debug("Converting Status Code %d", status_code)

    @staticmethod
    def get_files(customer,folder):
        front = open(folder + "/"+customer['idNo'] + '_F.png')
        back = open(folder + "/" + customer['idNo'] + '_B.png')
        files = {
            'front': front, 'back': back
        }
        return files
