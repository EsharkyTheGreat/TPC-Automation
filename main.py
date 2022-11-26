import requests
import bs4 
import re
LOGIN_URL="https://www.placement.iitbhu.ac.in/accounts/login/"
NOTICE_BOARD = "https://www.placement.iitbhu.ac.in/forum/c/notice-board/2022-23/"

s = requests.Session()
login_page_req = s.get(LOGIN_URL)
# CSRF Example - <input name="csrfmiddlewaretoken" type="hidden" value="wB8ByciHZfErIrkL0pOOJ2MHUqmx624z"/>
login_page_html = login_page_req.text
login_page_soup = bs4.BeautifulSoup(login_page_html,'html.parser')
# print(s.cookies)
# input_tag = login_page_soup.find('input')
# csrf_token = input_tag.attrs['value']
# print(csrf_token)
# s.cookies['csrftoken'] = csrf_token
s.headers['Referer'] = 'https://www.placement.iitbhu.ac.in/forum/'
s.headers['X-CSRFToken'] = s.cookies['csrftoken']
# print(s.cookies['csrftoken'])
login_data = {
    'csrfmiddlewaretoken' : s.cookies['csrftoken'],
    'login' : 'eshwar.s.che20@itbhu.ac.in',
    'password' : '123456'
}
res = s.post(LOGIN_URL,data=login_data)

notice_board_req = s.get(NOTICE_BOARD)
notice_board_soup = bs4.BeautifulSoup(notice_board_req.text,'html.parser')
all_table_elements = notice_board_soup.find_all('td',attrs={'class':'topic-name'})
# all_table_elements = notice_board_soup.find_all('')
all_links = []
for table_ele in all_table_elements:
    all_links.append(table_ele.a['href'])
    post_req = s.get("https://www.placement.iitbhu.ac.in/forum/c/notice-board/2022-23"+table_ele.a['href'])
    post_text = post_req.text
    print(re.findall('\D(\d{8})\D',post_text))
    
print(all_links)