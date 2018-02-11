import shutil
import cgi
import logging
import os
import uuid
import json


class Download:

    def __init__(self):
        pass

    def download(self,form,src,dst):
        if not form.has_key(src):
            logging.error("%s content is not present in the payload",src)
            return
        dst = open(dst, "wb")
        shutil.copyfileobj(form[src].file, dst)
        dst.close()

    def get_form(self,rfile,headers):
        form = cgi.FieldStorage(
            fp=rfile,
            headers=headers,
            environ={
                "REQUEST_METHOD": "POST",
                "CONTENT_TYPE": headers['Content-Type']
            })
        return form

    def get_folder(self):
        folder = "/tmp/" + str(uuid.uuid1())
        logging.debug("Temp folder is " + folder)
        os.mkdir(folder)
        return folder

    def download_all_content(self,rfile,headers):
        folder = self.get_folder()
        logging.debug("Downloading of Excel and image zip")
        form = self.get_form(rfile,headers)
        self.download_from_form(form,folder)
        return folder

    def download_from_form(self,form,folder):
        self.download(form,"file",folder+"/temp.xlsx")
        self.download(form,"images",folder+"/images.zip")


class DownloadContent(Download):
    def download_all_content(self,rfile,headers):
        folder = self.get_folder()
        form = self.get_form(rfile,headers)
        pay_load = json.loads(form.getvalue("data"))
        id_no = pay_load.get("id_no")
        if not id_no:
            logging.error("Payload does not contain id_no. Unable to process")
            return
        self.download(form, "front",folder + "/"+str(id_no)+"_F.png")
        self.download(form, "back",folder + "/"+str(id_no) + "_B.png")
        return folder,pay_load