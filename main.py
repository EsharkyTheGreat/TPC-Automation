import requests
import bs4
import re
import shutil
import esharky
import config
import csv
from aadeesh_bhaskar import *

LOGIN_URL = "https://www.placement.iitbhu.ac.in/accounts/login/"
NOTICE_BOARD = "https://www.placement.iitbhu.ac.in/forum/c/notice-board/2022-23/"

s = requests.Session()
login_page_req = s.get(LOGIN_URL)

EmailRegex = re.compile(r"[\w\.-]+@[\w\.-]+\.[\w]+")

login_page_html = login_page_req.text
login_page_soup = bs4.BeautifulSoup(login_page_html, 'html.parser')
s.headers['Referer'] = 'https://www.placement.iitbhu.ac.in/forum/'
s.headers['X-CSRFToken'] = s.cookies['csrftoken']
login_data = {
    'csrfmiddlewaretoken': s.cookies['csrftoken'],
    'login': config.EMAIl,
    'password': config.PASSWORD}

#Metadata
res = s.post(LOGIN_URL, data=login_data)
company_without_any_chemical = []
all_companies = []

for i in range(44):
    notice_board_req = s.get(NOTICE_BOARD+f'?page={i+1}')
    notice_board_soup = bs4.BeautifulSoup(notice_board_req.text, 'html.parser')
    all_table_elements = notice_board_soup.find_all(
        'td', attrs={'class': 'topic-name'})

    for table_ele in all_table_elements:
        link_suffix = table_ele.a['href']
        if 'shortlist' in link_suffix and '-ft' in link_suffix and 'interview' in link_suffix:
            ROLL_NOS = []
            EMAIL_IDS = []

            company_name = link_suffix.split("/")[-2]
            post_req = s.get(
                "https://www.placement.iitbhu.ac.in/"+link_suffix).text
            contentSoup = bs4.BeautifulSoup(post_req, 'html.parser')
            content = contentSoup.find(
                'td', attrs={'class': 'post-content'})
            rolls = re.findall('\d{8}', content.text)

            print(company_name)
            all_companies.append([company_name,"DONE", "https://www.placement.iitbhu.ac.in/"+link_suffix])

            # Converting roll numbers to CSV
            # esharky.createCSV(len(rolls), None,None,rolls,[company_name]*len(rolls))

            if len(rolls) == 0:
                # Must Be CSV or ODS
                link = contentSoup.find("div", attrs={"class": "attachments"})
                if len(link.text) > 0:
                    linkObject = link.a["href"]
                    if "csv" in linkObject:
                        print("CSV")
                        # Parse CSV
                        with s.get("https://www.placement.iitbhu.ac.in/" + linkObject) as r:
                            email, roll = parseCSV(r.content)
                            esharky.createCSV(len(roll), None, email, roll, [
                                              company_name]*len(roll))
                    elif "ods" in linkObject:
                        with s.get("https://www.placement.iitbhu.ac.in/" + linkObject) as r:
                            with open('./data.ods', "wb") as f:
                                f.write(r.content)
                        esharky.convertODStoCSV("./data.ods")
                        with open("./data.csv", "rb") as f:
                            email, roll = parseCSV(f.read())
                        esharky.createCSV(len(roll), None, email, roll, [
                                          company_name]*len(roll))
                    elif "xlsx" in linkObject:
                        # TODO: Parse xlsx
                        all_companies[-1][1] = "XLSX"
                        print("XLSX")

                # can be a case where name and email is provided and rolls is 0.
                else:
                    matchEmailOrRoll(content, ROLL_NOS, EmailRegex,
                                     EMAIL_IDS, company_without_any_chemical, company_name)

            else:
                matchEmailOrRoll(content, ROLL_NOS, EmailRegex,
                                 EMAIL_IDS, company_without_any_chemical, company_name)
                # Check for Name and Mail and write
                #                content_split = content.text.split(" ")
                #                for ele in content_split:
                #                    if "che19" in ele:
                #                        x = re.findall('[A-Za-z0-9.]*.che19@i?itbhu\.ac\.in',ele)[0]
                #                        EMAIL_IDS.append(x)
                #                    elif "@" in ele:
                #                        x = re.findall('[A-Za-z0-9.]*.com',ele)[0]
                #                        EMAIL_IDS.append(x)
                #                    if "19045" in ele:
                #                        x = re.findall('\d{8}',ele)[0]
                #                        ROLL_NOS.append(x)
                #


with open("./noRecords.csv", "w") as f:
    f.write("Company Name, Status, Link\n")
    for i in all_companies:
        if i[0] in company_without_any_chemical:
            i[1] = "NO RECORD"
        f.write(','.join(i))
        f.write('\n')

