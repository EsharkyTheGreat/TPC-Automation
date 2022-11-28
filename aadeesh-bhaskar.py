import csv
import re


#Bhaskar's Code

def parseCSV(contentBytes):
    roll = []
    email = []

    decoded_content = contentBytes.decode('utf-8')
    cr = csv.reader(decoded_content.splitlines(), delimiter=',')

    my_list = list(cr)

    for i in my_list:
        # kuch bhi nahi mila
        rollMila = False
        emailMila = False

        for j in i:
            # rolls = re.findall('\d{8}', j)
            if '19045' in j:
                rollMila = True
                roll.append(j)
                continue
            elif '.che19@' in j:
                emailMila = True
                #x = re.findall('[A-Za-z0-9.]*che19@i?itbhu\.ac\.in',j)
                email.append(j)
            elif 'itbhu.ac.in' not in j and 'iitbhu.ac.in' not in j and '@' in j:
                emailMila = True
                email.append(j)

        if not rollMila and not emailMila:
            continue
        if rollMila == False:
            roll.append("None")
        if emailMila == False:
            email.append("None")

    return email, roll
