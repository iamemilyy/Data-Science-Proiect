from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup as bs
import pandas as pd
import time
import random

#크롤링할 페이지열기
driver = webdriver.Chrome(r'chromedriver')
driver.implicitly_wait(10)
driver.get('https://everytime.kr/login')  # 에브리타임 로그인페이지로 이동

# 접속
driver.find_element(By.NAME, 'userid').send_keys('')  # 아이디
time.sleep(0.5)
driver.find_element(By.NAME, 'password').send_keys('') # 비밀번호
time.sleep(0.5)
driver.find_element(By.XPATH, '/html/body/div[1]/form/div/div/div/iframe').click() # 봇이 아닙니다 클릭
time.sleep(60)
driver.find_element(By.XPATH, '/html/body/div[1]/form/p[3]/input').click()  # 로그인 클릭
time.sleep(10)

# 자유게시판 크롤링
driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/ul/li[1]').click()  # 자유게시판 클릭
driver.implicitly_wait(10)

free_title = []  # 자유게시판의 게시물 제목
free_body = []  # 자유게시판의 게시물 본문
free_p_time = []  # 자유게시판 게시물의 작성시간

page_number = 2  # 시작 페이지

while page_number < 52:  # 마지막 페이지
    driver.implicitly_wait(1)
    html = driver.page_source
    soup = bs(html, 'html.parser')

    content = soup.findAll('article')
    
    for url in content:
        time.sleep(random.randint(2, 5))

        find_title = url.findAll('h2', {'class', 'medium'})

        for title in find_title:  # 각 게시물 제목 추출
            free_t = title.text
            free_title.append(free_t)

        find_body = url.findAll('p', {'class', 'small'})

        for body in find_body:  # 각 게시물 본문 추출
            free_b = body.text
            free_body.append(free_b)

        find_p_time = url.findAll('time', {'class', 'small'})

        for time_post in find_p_time:  # 각 게시물 작성시간 추출
            free_p_t = time_post.text
            free_p_time.append(free_p_t)

    time.sleep(1)
    driver.get('https://everytime.kr/386022/p/' + str(page_number))
    page_number += 1

driver.close()
grad_df = pd.DataFrame({'post time' : free_p_time, 'title' : free_title, 'body' : free_body})

grad_df.to_csv(r'free_board_crawling.csv', encoding='utf-8-sig')