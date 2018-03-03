import logging
import requests
import c
import httplib
import os
import fnmatch


class CustomerOperation:
    
    def __init__(self, folder):
        self.folder = folder

    def start_customer_on_boarding(self, headers, customer):
        create_customer_status_code = self.register_customer(self,headers, customer)
        if create_customer_status_code == httplib.OK:
            update_images_status_code = self.update_images(self,headers,customer,self.get_files(customer,self.folder))
            if update_images_status_code == httplib.OK:
                approve_customer_status_code = self.approve_customer(self,headers,customer)
                if approve_customer_status_code == httplib.OK:
                    convert_customer_status_code = self.convert_customer(self,headers,customer)
                    if convert_customer_status_code == httplib.OK:
                        return "Success",200
                    else:
                        return "Convert Customer", convert_customer_status_code
                return "Approve Customer", approve_customer_status_code
            else:
                return "Update Images", update_images_status_code
        else:
            return "Create Customer", create_customer_status_code



    @staticmethod
    def register_customer(self, headers, customer):
        logging.debug("Registering Customer %s ", customer.get('customerName'))
        return requests.post(c.site + "/customers", verify=False, headers=headers, data=customer).status_code


    @staticmethod
    def update_images(self, headers, customer, files):
        logging.debug("Updating images of " + customer.get('customerName'))
        return requests.put(c.site + "/customers/" + customer['idNo'], verify=False,
                                            headers=headers, data=customer, files=files).status_code

    @staticmethod
    def approve_customer(self, headers, customer):
        logging.debug("Approve " + customer.get('customerName'))
        return requests.post(c.site + "/customers/" + customer['idNo'] + "/approve", verify=False, headers=headers,
                                 data={}).status_code

    @staticmethod
    def validate_customer(self, headers, customer):
        logging.debug("Validating Customer %s", customer.get('customerName'))
        return requests.put(c.site + "/customers/" + customer['idNo'] + "/validate", verify=False, headers=headers,
                                data={}).status_code


    @staticmethod
    def convert_customer(self, headers, customer):
        logging.debug("Converting Customer %s", customer.get('customerName'))
        response = requests.post(c.site + "/customers/" + customer['idNo'] + "/convert-by-agent", verify=False,
                                 headers=headers, data={})
        return response.status_code

    @staticmethod
    def get_files(customer, folder):
        files = {
            'front': open(folder + "/" + customer['front_file']), 'back': open(folder + "/" + customer['back_file'])
        }
        return files
