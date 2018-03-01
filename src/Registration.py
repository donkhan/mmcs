import shutil
import auth
import logging


class Registration:

    def __init__(self):
        #self.headers = {"Api-key": auth.auth()}
        self.headers = {}

    def done(self):
        logging.debug("Going to delete %s",self.folder)
        shutil.rmtree(self.folder)
        logging.debug("Deleted %s",self.folder)







