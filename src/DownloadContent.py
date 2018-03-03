from Download import *


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