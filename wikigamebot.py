from helium import *
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import requests
from bs4 import BeautifulSoup
import re

def getLinks(article):
    headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36',
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
    }
    page = requests.get("https://en.wikipedia.org/wiki/"+article,headers=headers)
    page = BeautifulSoup(page.text,'html.parser')
    Links = set()
    for i in page.find_all('div',{'class':'reflist'}):
        i.decompose()
    for i in page.find_all('div',{'class':'navbox'}):
        i.decompose()
    for link in page.find('div',{'id':'mw-content-text'}).find_all("a",href=re.compile("^(/wiki/)((?!:).)*$")):
        if 'href' in link.attrs:
            Links.add(link.attrs['href'][6:])
    return list(Links)

driver = start_chrome('https://www.thewikigame.com')
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
driver.find_element_by_css_selector('.switch-login-link.seperate-login-link').click()
driver.find_element_by_name('username').send_keys('YOUR_USERNAME')
driver.find_element_by_name('password').send_keys('YOUR_PASSWORD')
click('LOGIN')
blyat = True
try:
    number = int(driver.find_element_by_tag_name('small').text.replace('s',''))
    if number < 40:
        time.sleep(number)
except:
    pass
while True:
    WebDriverWait(driver,150).until(EC.presence_of_element_located((By.ID, 'playNowButton'))).click()
    game = [i.text.replace(' ','%20').replace("'",'%27') for i in driver.find_elements_by_class_name('link')]
    print(game[0])
    print(game[1])
    if blyat:
        driver.execute_script('window.open()')
        blyat = False
    driver.switch_to.window(driver.window_handles[1])
    driver.get('https://www.sixdegreesofwikipedia.com/?source='+game[0]+'&target='+game[1])
    driver.find_element_by_tag_name('button').click()
    p = driver.find_element_by_tag_name('body').text
    while 'Found' not in p:
        time.sleep(0.5)
        p = driver.find_element_by_tag_name('body').text

    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(0.2)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height  

    croaks = []
    solutions = driver.find_elements_by_class_name('lazyload-wrapper')
    for i in solutions:
        croaks.append([j.get_attribute('href')[30:] for j in i.find_elements_by_tag_name('a')])
    driver.switch_to.window(driver.window_handles[0])
    for c in croaks:
        for i in range(1,len(c)):
            if c[i] not in getLinks(c[i-1]):
                break
        else:
            try:
                for i in range(1,len(c)):
                    actions = ActionChains(driver)
                    actions.move_to_element(driver.find_element_by_xpath('//a[@href="/wiki/'+c[i]+'"]')).click().perform()
                    print('Clicked',c[i])
                    time.sleep(2)
                driver.find_element_by_css_selector('.h3.mb-0').click()
                print('Done')
                time.sleep(1)
            except:
                print('Something went wrong')
                break