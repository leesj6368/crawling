from bs4 import BeautifulSoup
import requests 
import re
from selenium import webdriver
import time
from webdriver_manager.chrome import ChromeDriverManager


# BeautifulSoup 객체만들기
def create_soup(url):
    headers = {
        'User-Agent': ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36')

}

    response = requests.get(url, headers=headers)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'lxml')
    return soup

def scrape_english():

    print('([오늘의 회화 영어]]')
    url = 'https://www.hackers.co.kr/?c=s_eng%2Feng_contents%2FI_others_english'
    soup = create_soup(url)
    sentences = soup.find_all('div', attrs={'id':re.compile('^conv_kor_t')})
    print('\n영어지문')

    for sentence in sentences[len(sentences)//2:]: 
        print(sentence.get_text().strip())
    print('\n한글지문')
    for sentence in sentences[:(len(sentences)//2)]: # © 4 // 2 Af Schoey
        print(sentence.get_text().strip())

    options = webdriver.ChromeOptions()
    options.headless = True
    options.add_argument('window-size=1920x1080' )
    options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36')
    
    browser = webdriver.Chrome(ChromeDriverManager().install())
    url = 'https://www.hackers.co.kr/?c=s_eng%2Feng_contents%2FI_others_english'

    browser.get(url)
    time.sleep(2)
    sentences = browser.find_elements_by_class_name('^conv_sub')
    p_tag = WebDriverWait(browser,timeout=5).until(EC.presence_of_element_located((By.TAG_NAME, "p")))
    print('\n<<영어지문>>\n')

    for sentence in sentences[len(sentences)//2:]: 
        print(sentence.text.strip())

    print('\n<<한글지문>>\n')

    for sentence in sentences[:(len(sentences)//2)]: 
        print(sentence.text.strip())

if __name__=='__main__':
    scrape_english()