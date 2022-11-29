import csv
import esharky
import re


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


def matchEmailOrRoll(content, ROLL_NOS, EmailRegex, EMAIL_IDS, company_without_any_chemical, company_name):
    lines = content.get_text(strip=True, separator='\n')
    for line in lines.split():
        x = re.findall('19045\d{3}', line)
        if len(x) > 0:
            ROLL_NOS.extend(x)
        else:
            for email in EmailRegex.findall(line):
                if '.che19' in email:
                    EMAIL_IDS.append(email)
                elif not '@itbhu.ac.in' in email and not '@iitbhu.ac.in' in email:
                    EMAIL_IDS.append(email)

    if len(ROLL_NOS) > 0:
        esharky.createCSV(len(ROLL_NOS), None, None, ROLL_NOS, [
            company_name]*len(ROLL_NOS))
    elif len(EMAIL_IDS) > 0:
        esharky.createCSV(len(EMAIL_IDS), None, EMAIL_IDS, None, [
            company_name]*len(EMAIL_IDS))
    else:
        print("NO RECORDS IN", company_name)
        company_without_any_chemical.append(company_name)
