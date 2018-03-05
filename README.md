MaxMoney Customer Onboarding Service.

Python Project. Packages Installed: xlrd

pip install xlrd

Registration of Customers through excel file: 
curl -i -X POST -H "Content-Type: multipart/form-data" -F "file=@/tmp/T.xlsx" -F "images=@/Users/kkhan/Downloads/images.zip" http://127.0.0.1:6667/register/customers

Single Registration of a Customer
curl -i -X POST -H "Content-Type: multipart/form-data"  -F "front=@/Users/kkhan/Downloads/f.png;filename=a.png" -F "back=@/Users/kkhan/Downloads/b.png;filename=b.png" -F "data={\"id_no\":3456,\"doc_type\":\"NRIC\" ,\"name\":\"afzal\"};type=application/json"  http://127.0.0.1:6667/register/customer
