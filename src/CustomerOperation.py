import logging
import requests
import c
import httplib
import json


class CustomerOperation:
    
    def __init__(self, folder):
        self.folder = folder

    def start_customer_on_boarding(self, headers, customer):
        fns = [self.register_customer,self.update_images,self.approve_customer,self.convert_customer]
        operation_names = ['Create Customer','Upload Images',"Approve Customer","Conversion of Customer"]
        files = self.get_files(customer,self.folder)
        res = {
            'name' : customer.get('fullName'),
            'status_code' : httplib.OK,
            'status_text' : " registered successfully ",
            'step' : ' All Steps Done '
        }
        for t in zip(fns,operation_names):
            response = t[0](self,headers,customer,files)
            if response.status_code != httplib.OK:
                res['status_code'] = response.status_code
                res['status_text'] = json.loads(response.content)
                #print json.loads(response.content)
                res['step'] = t[1]
                return res

        return res

    @staticmethod
    def register_customer(self, headers, customer,files):
        logging.debug("Registering Customer %s ", customer.get('customerName'))
        print customer
        return requests.post(c.site + "/customers", verify=False, headers=headers, data=customer)


    @staticmethod
    def update_images(self, headers, customer, files):
        logging.debug("Updating images of " + customer.get('customerName'))
        return requests.put(c.site + "/customers/" + customer['idNo'], verify=False,
                                            headers=headers, data=customer, files=files)

    @staticmethod
    def approve_customer(self, headers, customer,files):
        logging.debug("Approve " + customer.get('customerName'))
        return requests.post(c.site + "/customers/" + customer['idNo'] + "/approve", verify=False, headers=headers,
                                 data={})

    @staticmethod
    def validate_customer(self, headers, customer,files):
        logging.debug("Validating Customer %s", customer.get('customerName'))
        return requests.put(c.site + "/customers/" + customer['idNo'] + "/validate", verify=False, headers=headers,
                                data={})

    @staticmethod
    def convert_customer(self, headers, customer,files):
        logging.debug("Converting Customer %s", customer.get('customerName'))
        return requests.post(c.site + "/customers/" + customer['idNo'] + "/convert-by-agent", verify=False,
                                 headers=headers, data={})

    @staticmethod
    def get_files(customer, folder):
        files = {
            'front': open(folder + "/" + customer['front_file']), 'back': open(folder + "/" + customer['back_file'])
        }
        return files
