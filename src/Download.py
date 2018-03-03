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
    def download(form,src,dst_folder,file_name,ext="ukn"):
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
        return dst.name

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
        logging.debug("Downloading of Excel/CSV and image zip")
        form = self.get_form(r_file,headers)
        self.download_from_form(form,self.folder)
        return (self.folder, self.file_name)

    def download_from_form(self,form,folder):
        self.file_name = self.download(form,"file",folder,"temp")
        self.download(form,"images",folder,"images","zip")

