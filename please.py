from bs4 import BeautifulSoup
import urllib.request
import requests
import re
from selenium import webdriver
import datetime
import os
import telegram

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.22 Safari/537.36'}

def create_soup(url):
  result = requests.get(url, headers=headers)
  result.raise_for_status()
  soup = BeautifulSoup(result.text, "lxml")
  return soup

# 1. 네이버 오늘의 {서울} 날씨(today_weather)
def scrape_weather(): 
    print("[오늘의 날씨]")
    url='https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=1&ie=utf8&query=%EB%82%A0%EC%94%A8'
    soup = create_soup(url)
    
  #기온(현재, 최고, 최저)
    cast = soup.find(class_='temperature_text').get_text() #cast = soup.find('p', class_='cast_txt').get_text 에서 수정
    min_temp = soup.find('span', class_='lowest').get_text() #min_temp = soup.find('span', class_='min').get_text() 에서 수정
    max_temp = soup.find('span', class_='highest').get_text() #max_temp = soup.find('span', class_='max').get_text() 에서 수정
    
    #강수량
    rain_rate = soup.find('span', class_='rainfall').get_text().strip()
    
    #미세먼지
    dust = soup.find('span', class_='txt').get_text()

    message = f"[오늘의 날씨]\n현재{cast}\n(최저 {min_temp} / 최고 {max_temp})\n강수확률 {rain_rate}% \n미세먼지 {dust}\n\n\n"
    save_to_txt(message)

# 2. 오늘의 네이버 it 뉴스

def scrape_it_news():
    print("[오늘의 IT 뉴스]")
    itnews_url = "https://news.naver.com/main/list.nhn?mode=LS2D&mid=shm&sid1=105&sid2=230"
    soup = create_soup(itnews_url)

    it_list = soup.find("ul", attrs={"class": "type06_headline"}).find_all("li", limit=3)
    for index, news in enumerate(it_list):
      a_idx = 0
      img = news.find("img")
      if img:
        a_idx = 1 # 이미지(img)가 있을 경우 해당 a 태그를 사용
      title = news.find_all("a")[a_idx].get_text().strip()
      link = news.find_all("a")[a_idx]["href"]
      message = f"[오늘의 IT 뉴스]\n{index+1}. {title}\n({link})\n\n\n"
      save_to_txt(message)

# 3. 오늘의 인기 주식 종목
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
        message = f"[오늘의 주식]\n{title}\n({result})\n\n\n"
        save_to_txt(message)

# 4. 해커스토익에서 오늘의 영어회화 가져오기
def scrape_english():
  print("[오늘의 영어회화]")
  hackers_url = "https://www.hackers.co.kr/?c=s_eng/eng_contents/I_others_english&keywd=haceng_submain_lnb_eng_I_others_english&logger_kw=haceng_submain_lnb_eng_I_others_english"
  soup = create_soup(hackers_url)

  eng = soup.find_all("div", attrs={"class": "conv_txt"})[1].get_text().strip().replace("\n\n", "\n").replace("\n\n", "\n")
  kor = soup.find_all("div", attrs={"class": "conv_txt"})[0].get_text().strip().replace("\n\n", "\n").replace("\n\n", "\n")

  message = f"[오늘의 영어회화]\n(영어지문)\n{eng}\n\n(한글지문)\n{kor}\n"
  save_to_txt(message)

# 전체 동작 한번에 실행
def run_butler():
  scrape_weather()  # 네이버에서 오늘의 날씨 가져오기
  scrape_it_news() # 네이버에서 오늘의 헤드라인 뉴스 상위 3개 가져오기
  scrape_share_price() # 네이버에서 오늘의 IT 헤드라인 뉴스 상위 3개 가져오기
  scrape_english()  # 해커스영어에서 오늘의 영어회화 가져오기

# txt 파일로 저장
def save_to_txt(msg):
  BASE_PATH = "/Users/leesj/Downloads/"
  today_string = datetime.datetime.today().strftime('%Y%m%d') # 파일명을 년월일로.
  filename = f"butler_{today_string}.txt" # 파일명 변수 지정.
  file = open(f"{BASE_PATH}{filename}", mode="a", encoding="utf-8") # 파일 만들기. "w"는 (덮어)쓰기 모드. "a"는 연속으로 이어 쓰기 모드.  
  file.write(msg) # msg 내용을 앞서 연 file 에 쓰기
  file.close() # 파일 닫기

# 텔레그램으로 전송하기 (메시지가 길 경우 에러 발생)
def send_to_telegram():
  bot = telegram.Bot(token="5555815826:AAESmlH829POH_XfKdLzL9E8W1rSH1RZM2E")
  BASE_PATH = "/Users/leesj/Downloads/"
  today_string = datetime.datetime.today().strftime('%Y%m%d')
  filename = "butler_" + today_string + ".txt"
  file = open(BASE_PATH + filename, mode="r", encoding="UTF-8")  # 읽기 모드로 파일 열기
  text = file.read() # text 파일 속 내용 전체를 읽어 문자열(str) 형태로 반환
  # text = file.readline() # text 파일의 첫 줄을 읽어들여 문자열로 반환
  # text = file.readlines() # text 파일 속 내용 전체를 읽어 리스트(list) 형태로 반환
  try:
    bot.sendMessage(chat_id=-5555815826, text=text)
    
    print("전송을 완료했습니다.")
  except:
    print("전송 중 에러가 발생했습니다.")
  # 내용 전송 후 해당 파일 삭제. 불필요한 파일이 쌓이거나 내용이 중복돼 쌓이는 걸 방지하기 위해.
  return 


if __name__ == "__main__":
  run_butler()
  send_to_telegram()