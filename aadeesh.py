import csv
import re


def parseCSV(contentBytes):
    roll = []
    email = []

    decoded_content = contentBytes.decode('utf-8')
    cr = csv.reader(decoded_content.splitlines(), delimiter=',')

    my_list = list(cr)

    for i in range(len(my_list)):
        # kuch bhi nahi mila
        rollMila = False
        emailMila = False

        for j in my_list[i]:
            rolls = re.findall('\d{8}', j)

            if rolls:
                rollMila = True
                roll.append(rolls)
                continue
            if '@' in j:
                emailMila = True
                email.append(j)
                continue

        if rollMila == False:
            rolls.append("None")
        if emailMila == False:
            email.append("None")

    return zip(email, roll)
