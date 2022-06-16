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


if __name__=='__main__':
    scrape_it_news()
 