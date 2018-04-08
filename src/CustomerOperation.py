import logging
import requests
import httplib
import ConfigParser


class CustomerOperation:
    
    def __init__(self, folder):
        self.folder = folder
        config = ConfigParser.ConfigParser()
        config.read("conf/application.conf")
        self.site = config.get("credentials","site")
        self.url = config.get('validate','url')

    def start_customer_on_boarding(self, headers, customer):
        fns = [self.register_customer,self.update_images,self.approve_customer,self.validate_customer,self.convert_customer,self.activate_user]
        operation_names = ['Create Customer','Upload Images',"Approve Customer","Validating Customer","Convert Customer","Activate User"]
        files = self.get_files(customer,self.folder)
        res = {
            'name': customer.get('fullName'),
            'status_code': httplib.OK,
            'status_text': " Registered Successfully ",
            'step': ' All Steps Done '
        }
        for t in zip(fns,operation_names):
            response = t[0](self,headers,customer,files)
            status_code = response.status_code
            print t[0], response.status_code
            if status_code < 200 or status_code > 299:
                res['status_code'] = response.status_code
                res['step'] = t[1]
                res['status_text'] = 'Error in execution'
                return res

        return res

    @staticmethod
    def validate_customer(self,headers,customer,files):
        logging.debug("Validating Customer %s ", customer.get('customerName'))
        post_data = {
            'url' : self.url,
            'status' : 'Validated'
        }
        return requests.post(self.site + "/customers/" + customer.get('idNo') + "/validate",
                             verify=False, headers=headers, data=post_data)

    @staticmethod
    def register_customer(self, headers, customer,files):
        logging.debug("Registering Customer %s ", customer.get('customerName'))
        return requests.post(self.site + "/customers", verify=False, headers=headers, data=customer)


    @staticmethod
    def update_images(self, headers, customer, files):
        logging.debug("Updating images of " + customer.get('customerName'))
        return requests.put(self.site + "/customers/" + customer['idNo'], verify=False,
                                            headers=headers, data={}, files=files)

    @staticmethod
    def approve_customer(self, headers, customer,files):
        logging.debug("Approve " + customer.get('customerName'))
        return requests.post(self.site + "/customers/" + customer['idNo'] + "/approve", verify=False, headers=headers,
                                 data={})

    @staticmethod
    def convert_customer(self, headers, customer,files):
        logging.debug("Converting Customer %s", customer.get('customerName'))
        return requests.post(self.site + "/customers/" + customer['idNo'] + "/convert-by-agent", verify=False,
                                 headers=headers, data={})

    @staticmethod
    def activate_user(self,headers,customer,files):
        user_name = str(customer['email']).lower()
        print user_name
        logging.debug("Activating User %s", user_name)
        return requests.put(self.site + "/users/" + user_name, verify=False,
                             headers=headers, data={'status' : 'active'})

    @staticmethod
    def get_files(customer, folder):
        files = {
            'front': open(folder + "/" + customer['front']), 'back': open(folder + "/" + customer['back'])
        }
        return files
