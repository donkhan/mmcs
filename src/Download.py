import shutil
import cgi
import logging
import os
import uuid
import json


class Download:

    def __init__(self):
        self.folder = "/tmp/" + str(uuid.uuid1())
        logging.debug("Temp folder is " + self.folder)
        os.mkdir(self.folder)

    @staticmethod
    def download(form,src,dst_folder,file_name,ext):
        if not form.has_key(src):
            logging.error("%s content is not present in the payload",src)
            return
        if form[src].filename is not None:
            ext = str(form[src].filename)
            ext = ext[ext.rindex(".")+1:]
        dst = dst_folder + "/" + file_name  + "." + ext
        dst = open(dst, "wb")
        shutil.copyfileobj(form[src].file, dst)
        dst.close()

    @staticmethod
    def get_form(r_file,headers):
        form = cgi.FieldStorage(
            fp=r_file,
            headers=headers,
            environ={
                "REQUEST_METHOD": "POST",
                "CONTENT_TYPE": headers['Content-Type']
            })
        return form

    def download_all_content(self,r_file,headers):
        logging.debug("Downloading of Excel and image zip")
        form = self.get_form(r_file,headers)
        self.download_from_form(form,self.folder)
        return self.folder

    def download_from_form(self,form,folder):
        self.download(form,"file",folder,"temp","xlsx")
        self.download(form,"images",folder,"images","zip")


class DownloadContent(Download):
    def download_all_content(self,r_file,headers):
        form = self.get_form(r_file,headers)
        pay_load = json.loads(form.getvalue("data"))
        id_no = pay_load.get("id_no")
        if not id_no:
            logging.error("Payload does not contain id_no. Unable to process")
            return
        self.download(form,"front",self.folder,str(id_no)+"_F","png")
        self.download(form,"back",self.folder,str(id_no) + "_B","png")
        return self.folder,pay_load