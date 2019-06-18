import requests
import webbrowser
import csv
import re
import numpy as np



from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

def clean_text(text):
    cleaned_text = re.sub('[a-zA-z]','',text)
    cleaned_text = re.sub('[\{\}\[\]\/?.,;:|\)*~`!^\-_+<>@\#$%&\\\=\(\'\"\♥\♡\ㅋ\ㅠ\ㅜ\ㄱ\ㅎ\ㄲ\ㅡ]',' ',cleaned_text)
    RE_EMOJI = re.compile('[\U00010000-\U0010ffff]', flags=re.UNICODE)  # 이모티콘 문자 제거
    cleaned_text = RE_EMOJI.sub(r'', cleaned_text)
    hangul = re.compile('[^ ㄱ-ㅣ가-힣0-9]+')
    cleaned_text = hangul.sub('', cleaned_text)
    return cleaned_text


driver = webdriver.Chrome('chromedriver')   #드라이버 위치
url = 'https://instogram.pro/tag/'  #검색 홈페이지
keyword = '20대' #검색할 내용
driver.get('https://instogram.pro/location/2123028574680745') #드라이버에 전달   #버튼 객체 가져오기


#more information button click  HEAD
for i in range(1000):
    try:
        button = driver.find_element_by_xpath("//*[@id='tagLoadMore']")
        button.click()
    except NoSuchElementException:  # spelling error making this code not work as expected
        pass
#TAIL

post = driver.find_elements_by_class_name("post-content") #content 리스트

location = []
content = []
tag = []
for i in post:
    try:
        content_temp = i.find_element_by_class_name("content")  #content 노드 가져오기

        temp_text = clean_text(content_temp.text)   #content 내용 가져오기

        #tag_temp = content_temp.find_element_by_xpath('./p/a')
        #print(tag_temp.text)

        if(len(temp_text.replace(' ',''))!=0):
            content.append(temp_text)
            location.append(clean_text(i.find_element_by_class_name("location").text))  # 장소
        '''
        #tag string append to list
        for j in tag_temp:
            tag_str += j.text + ','
        tag.append(tag_str)
        '''

    except NoSuchElementException:
        pass

'''
for i in len(location):
    str = content[i] + ',' + location[i]
'''


save_data = np.stack([content, location], axis=1)
csvfile = open("../Dataset/Instagram.csv", "w", newline="", encoding='utf-8')
csvwriter = csv.writer(csvfile)
for row in save_data:
    csvwriter.writerow(row)
csvfile.close()


'''
req = requests.get('url + keyword')
html = req.text
soup =BeautifulSoup(html, 'html.parser')
content, location  = []
for i in soup.find_all(soup.self, class_='content'):
    content.append(i.get_text())
print(len(content))

for i in soup.find_all(soup.self, class_='location'):
    location.append(i.get_text())
'''