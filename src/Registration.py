import shutil
import auth
import logging
import ConfigParser


class Registration:

    def __init__(self):
        config = ConfigParser.ConfigParser()
        config.read("conf/application.conf")
        site = config.get("credentials","site")
        self.headers = {"Api-key": config.get('credentials','api-key')}
        #self.headers = {}

    def done(self):
        logging.debug("Going to delete %s",self.folder)
        shutil.rmtree(self.folder)
        logging.debug("Deleted %s",self.folder)







