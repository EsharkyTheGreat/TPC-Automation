import os
import sys

def convertODStoCSV(filpath):
    os.system(f"libreoffice --convert-to csv {os.path.abspath(filpath)}")

# IMPORTANT -- DOES NOT WRITE HEADINGS!!!
def createCSV(size,name,email,rollno,company):
    with open('./finalData.csv',"a") as f:
        for i in range(size):
            Name = Email = Rollno = Company = "None"
            if name: Name = name[i]
            if email: Email = email[i]
            if rollno: Rollno = rollno[i]
            if company: Company = company[i]
            content = f'{Name},{Email},{Rollno},{Company}\n'
            f.write(content)
