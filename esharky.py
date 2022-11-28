import os
import sys

def convertODStoCSV(filpath):
    os.system(f"libreoffice --convert-to csv {os.path.abspath(filpath)}")

def createCSV(headings,name,email,rollno,company,outfile):
    with open(outfile,"wb") as f:
        heading = ",".join(headings)
        f.write(heading)
        f.write('\n')
        for i in range(len(email)):
            name = name[i] or 'None'
            email = email[i] or 'None'
            rollno = rollno[i] or 'None'
            company = company[i] or 'None'
            content = f'{name},{email},{rollno},{company}\n'
            f.write(content)
    print(f"Wrote to {outfile}")