import shutil
import auth
import logging
import ConfigParser

class Registration:

    def __init__(self):
        config = ConfigParser.ConfigParser()
        config.read("conf/application.conf")
        user_name = config.get("credentials",'web-server-user')
        pass_word = config.get("credentials","web-server-password")
        #self.headers = {"Api-key": auth.auth(user_name,pass_word)}
        self.headers = {}

    def done(self):
        logging.debug("Going to delete %s",self.folder)
        shutil.rmtree(self.folder)
        logging.debug("Deleted %s",self.folder)







