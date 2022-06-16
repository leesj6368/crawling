from bs4 import BeautifulSoup
import requests 
import re
from selenium import webdriver
import time
# BeautifulSoup 객체만들기
def create_soup(url):
    headers = {
        'User-Agent': ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36')

}

    response = requests.get(url, headers=headers)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'lxml')
    return soup



def scrape_weather():
    print('[[ 오늘의 날씨]]/n')
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
    print(f' 강수확률 {rain_rate} /') #print(f'오전 {morning_rain_rate} / 오후 {afternoon_rain_rate}') 에서 수정
    print()
    print(f' 미세먼지 {dust}')  #미세먼지(좋음,보통,나쁨,매우)로 구분
    print()

if __name__=='__main__':
    scrape_weather()