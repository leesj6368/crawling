from bs4 import BeautifulSoup
import urllib.request
import requests
import re
from selenium import webdriver
import time
from webdriver_manager.chrome import ChromeDriverManager
from tkinter import *
import tkinter

def create_soup(url):
    headers = {
        'User-Agent': ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36')

}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'lxml')
    return soup

def scrape_weather():
    print("[[ 오늘의 날씨 ]]\n")
    url='https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=1&ie=utf8&query=%EB%82%A0%EC%94%A8'
    soup = create_soup(url)

    #기온(현재, 최고, 최저)
    cast = soup.find(class_='temperature_text') #cast = soup.find('p', class_='cast_txt').get_text 에서 수정
    min_temp = soup.find('span', class_='lowest') #min_temp = soup.find('span', class_='min').get_text() 에서 수정
    max_temp = soup.find('span', class_='highest') #max_temp = soup.find('span', class_='max').get_text() 에서 수정
    
    #강수량
    rain_rate = soup.find('span', class_='rainfall').get_text().strip()
    

    #미세먼지
    dust = soup.find('span', class_='txt').get_text()

    #출력
    print(cast.get_text()) #print(cast) 에서 수정
    print(f'{min_temp.get_text()} / { max_temp.get_text()}') #print(f'현재 {curr_temp} (최저 {min_temp} / 최고) {max_temp})') 에서 수정
    print()
    print(f' 강수확률 {rain_rate} ') #print(f'오전 {morning_rain_rate} / 오후 {afternoon_rain_rate}') 에서 수정
    print()
    print(f' 미세먼지 {dust}')  #미세먼지(좋음,보통,나쁨,매우)로 구분
    print()

def scrape_share_price():
    print("[[ 오늘의 주식 ]]\n")
    url='https://finance.naver.com/sise/' #주소를 변수에 넣기

    resp = urllib.request.urlopen(url) # url을 넣어 html형식으로 돌려받는다.
    soup = BeautifulSoup(resp,'html.parser',from_encoding='euc-kr') #불러올때 한글깨짐으로 encoding 설정
    sises = soup.find('ul',{'class' : 'lst_pop'}) # class가 lst_pop인 ul 태그를 찾는다.
    sises_kor = sises.select('li') # sises에서 li 태그를 찾음

    for sise in sises_kor: #반복
        title = sise.find('a').text  # a 태그를 text로 가져온다.
        result = sise.find('span').text # span 태그를 text로 가져온다.
        print(f'{title} \t {result}') # title과 result 출력

def scrape_it_news():
    print("[[ 오늘의 IT 뉴스 ]]\n")
    url="https://news.naver.com/main/list.naver?mode=LS2D&mid=shm&sid1=105&sid2=230"
    soup = create_soup(url)
    news_list = soup.find("ul",attrs={"class":"type06_headline"}).find_all("li", limit=5)
    for index, news in enumerate(news_list):
        a_idx=0
        img=news.find("img")
        if img:
            a_idx=1

        title=news.find_all("a")[a_idx].get_text().strip()
        link=news.find_all("a")[a_idx]["href"]
        print("{}. {}".format(index, title))
        print("   (링크 : {})".format(link)) 
    print()

def scrape_english():

    print('[[ 오늘의 회화 ]]')
    url = 'https://www.hackers.co.kr/?c=s_eng%2Feng_contents%2FI_others_english'
    soup = create_soup(url)
    sentences = soup.find_all('div', attrs={'id':re.compile('^conv_kor_t')})
    print('\n<< 영어지문 >>\n')

    for sentence in sentences[len(sentences)//2:]: 
        print(sentence.get_text().strip())
    print('\n<< 한글지문 >>\n')
    for sentence in sentences[:(len(sentences)//2)]: 
        print(sentence.get_text().strip())

    
######################GUI
win = Tk()
win.geometry("600x500")
win.title("하루의 시작, 온라인 비서 - 파개왕") 
win.option_add("*Font","돋움 20")
win.configure(bg='skyblue')

btn1 = Button(win) 
btn1.config(width=30, height=2) 
btn1.config(text="오늘의 인기 주식")
btn1.config(command = scrape_share_price) 
btn1.pack() 

btn2 = Button(win) 
btn2.config(width=30, height=2) 
btn2.config(text="오늘의 IT 뉴스")
btn2.config(command = scrape_it_news) 
btn2.pack() 

btn3 = Button(win) 
btn3.config(width=30, height=2) 
btn3.config(text="오늘의 영어 회화")
btn3.config(command = scrape_english) 
btn3.pack() 

btn4 = Button(win) 
btn4.config(width=30, height=2) 
btn4.config(text="오늘의 날씨")
btn4.config(command = scrape_weather) 
btn4.pack() 
win.mainloop()