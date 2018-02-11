import logging
import requests
import c
import httplib


class CustomerOperation:
    def __init__(self, uuid):
        self.folder = uuid

    def start_customer_on_boarding(self, headers, customer):
        self.start_chaining(self, headers, customer, self.get_files(customer, self.folder),
                            [self.register_customer, self.update_images, self.approve_customer,
                             self.convert_customer])

    def chain(self, operation, response, expected_status_code, headers, customer, files, next_functions):
        self.log_response_code(operation, response.status_code)
        if response.status_code == expected_status_code:
            next_functions[0](self, headers, customer, files, next_functions[1:])

    @staticmethod
    def start_chaining(self, headers, customer, files, next_functions):
        next_functions[0](self, headers, customer, files, next_functions[1:])

    @staticmethod
    def log_response_code(operation, status_code):
        logging.debug("%s %d", operation, status_code)

    @staticmethod
    def register_customer(self, headers, customer, files, next_functions):
        logging.debug("Registering Customer %s ", customer.get('customerName'))
        self.chain("Create Customer",
                   requests.post(c.site + "/customers", verify=False, headers=headers, data=customer),
                   httplib.OK, headers, customer, files, next_functions)

    @staticmethod
    def update_images(self, headers, customer, files, next_functions):
        logging.debug("Updating images of " + customer.get('customerName'))
        self.chain("Update Customer", requests.put(c.site + "/customers/" + customer['idNo'], verify=False,
                                            headers=headers, data=customer, files=files),httplib.OK, headers, customer,
                   files, next_functions)

    @staticmethod
    def approve_customer(self, headers, customer, files, next_functions):
        logging.debug("Approve " + customer.get('customerName'))
        self.chain("Approve Customer",
                   requests.post(c.site + "/customers/" + customer['idNo'] + "/approve", verify=False, headers=headers,
                                 data={}),
                   httplib.NO_CONTENT, headers, customer, files, next_functions)

    @staticmethod
    def validate_customer(self, headers, customer, files, next_functions):
        logging.debug("Validating Customer %s", customer.get('customerName'))
        self.chain("Validating Customer",
                   requests.put(c.site + "/customers/" + customer['idNo'] + "/validate", verify=False, headers=headers,
                                data={})
                   ,  httplib.OK, headers, customer, files, next_functions)

    @staticmethod
    def convert_customer(self, headers, customer, files, next_functions):
        logging.debug("Converting Customer %s", customer.get('customerName'))
        response = requests.post(c.site + "/customers/" + customer['idNo'] + "/convert-by-agent", verify=False,
                                 headers=headers, data={})
        self.log_response_code("Converting Customer", response.status_code)

    @staticmethod
    def get_files(customer, folder):
        front = open(folder + "/" + customer['idNo'] + '_F.png')
        back = open(folder + "/" + customer['idNo'] + '_B.png')
        files = {
            'front': front, 'back': back
        }
        return files
