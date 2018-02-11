import shutil
import cgi
import logging


class Download:

    def __init__(self):
        pass

    def download(self,form,src,dst):
        fdst = open(dst, "wb")
        shutil.copyfileobj(form[src].file, fdst)
        fdst.close()

    def download_file(self,rfile,headers):
        logging.debug("Downloading of Excel and image zip")
        form = cgi.FieldStorage(
            fp=rfile,
            headers=headers,
            environ={
                "REQUEST_METHOD": "POST",
                "CONTENT_TYPE": headers['Content-Type']
            })
        self.download(form,"file","/tmp/temp.xlsx")
        self.download(form,"images","/tmp/images.zip")
