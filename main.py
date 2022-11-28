import requests
import bs4 
import re

LOGIN_URL="https://www.placement.iitbhu.ac.in/accounts/login/"
NOTICE_BOARD = "https://www.placement.iitbhu.ac.in/forum/c/notice-board/2022-23/"

s = requests.Session()
login_page_req = s.get(LOGIN_URL)

login_page_html = login_page_req.text
login_page_soup = bs4.BeautifulSoup(login_page_html,'html.parser')
s.headers['Referer'] = 'https://www.placement.iitbhu.ac.in/forum/'
s.headers['X-CSRFToken'] = s.cookies['csrftoken']
login_data = {
    'csrfmiddlewaretoken' : s.cookies['csrftoken'],
    'login' : 'eshwar.s.che20@itbhu.ac.in',
    'password' : '123456'
}
res = s.post(LOGIN_URL,data=login_data)

notice_board_req = s.get(NOTICE_BOARD)
notice_board_soup = bs4.BeautifulSoup(notice_board_req.text,'html.parser')
all_table_elements = notice_board_soup.find_all('td',attrs={'class':'topic-name'})


for table_ele in all_table_elements:
    link_suffix = table_ele.a['href']
    if 'shortlist' in link_suffix and '-ft' in  link_suffix:
        post_req = s.get("https://www.placement.iitbhu.ac.in/"+link_suffix).text
        content = bs4.BeautifulSoup(post_req,'html.parser').find('td', attrs={'class': 'post-content'})
        rolls = re.findall('\d{8}',content.text)
        print(rolls)
        if len(rolls) == 0:
            print("https://www.placement.iitbhu.ac.in/"+link_suffix)

