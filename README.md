MaxMoney Customer Onboarding Service.

Python Project. Packages Installed: xlrd

Registration of Customers through excel file: 
curl -i -X POST -H "Content-Type: multipart/formdata" -F "file=@/tmp/T.xlsx" -F "images=@/Users/kkhan/Downloads/images.zip" http://127.0.0.1:6667/register/customers

Single Registration of a Customer
curl -i -X POST -H "Content-Type: multipart/mixed" -F "file=@/tmp/T.xlsx" -F "images=@/Users/kkhan/Downloads/images.zip"  -F "data={\"edipi\":123456789,\"firstName\":\"John\",\"lastName\":\"Smith\",\"email\":\"john.smith@gmail.com\"};type=application/json"  http://127.0.0.1:6667/register/customer
