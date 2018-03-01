from Registration import *
import zipfile
from CustomerOperation import *


class BulkRegistration(Registration):

    def __init__(self,folder):
        self.customer_operation = CustomerOperation(folder)
        self.folder = folder
        Registration.__init__(self)


    def extract_images(self,folder):
        zip_ref = zipfile.ZipFile(folder + "/images.zip", 'r')
        zip_ref.extractall(folder)
        zip_ref.close()

