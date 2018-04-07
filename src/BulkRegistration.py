from Registration import *
import zipfile
from CustomerOperation import *
import os


class BulkRegistration(Registration):

    def __init__(self,folder):
        self.customer_operation = CustomerOperation(folder)
        self.folder = folder
        Registration.__init__(self)

    @staticmethod
    def extract_images(folder):
        zip_ref = zipfile.ZipFile(folder + "/images.zip", 'r')
        zip_ref.extractall(folder)
        zip_ref.close()

    @staticmethod
    def get_file(front,back,folder):
        print "Folder " + folder
        files = os.listdir(folder)
        print " Files " + files
        new_front = ''
        new_back = ''
        for file in files:
            if file.split(".")[0] == front:
                new_front = file
            if file.split(".")[0] == back:
                new_back = file
        return new_front,new_back


