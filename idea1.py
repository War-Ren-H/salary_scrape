from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

import traceback
import time
import requests
from bs4 import BeautifulSoup
from xlwings.constants import TimeUnit

#Start the automation
path = r"C:\Users\Statistician X\Downloads\chromedriver_win32\chromedriver.exe"
options = Options()
#options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

wd = webdriver.Chrome(path, chrome_options = options)
#wd = webdriver.Safari()
url = 'https://www.levels.fyi/comp.html?track=Data%20Scientist&region=819'
wd.get(url)

element = WebDriverWait(wd,10).until(EC.presence_of_element_located((By.CLASS_NAME,'dropdown')))
element.click()
time.sleep(0.2)
element = WebDriverWait(wd,10).until(EC.presence_of_element_located((By.XPATH,'/html/body/div[3]/div[2]/div[4]/div/div[1]/div[1]/div[3]/div[1]/span[2]/span/ul/li[4]')))
element.click()
time.sleep(0.2)

link_list = []
#while len(wd.current_url) <= len(url):
    for i in range(10):
        #Open all of the tabs
        #for j in range(20):
            #xpath = '//*[@id="compTable"]/tbody/tr[{}]/td[3]'.format(str(j+1))
            #element = WebDriverWait(wd, 50).until(EC.presence_of_element_located((By.XPATH, xpath)))
            #element.click()
            #print("detail: ", j)
    
        for j in range(1,180):
            try:
                xpath = '//*[@id="compTable"]/tbody/tr[{}]'.format(str(j))
                element = WebDriverWait(wd, 50).until(EC.presence_of_element_located((By.XPATH, xpath)))
                element.click()
                time.sleep(0.01)
                print("detail: ", j)
            except:
                pass

    #Extract the relevant links
        page_source = wd.page_source

        soup = BeautifulSoup(page_source, 'lxml')
        links = soup.find_all("div", {"class": "direct-offer-link"})
        for l in links:
            z = l.find('a').get('href')
            link_list.append('levels.fyi' + z)
            print(l)
    
    #Click next button
        # element2 = WebDriverWait(wd, 50).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.page-next a')))
        time.sleep(0.5)
        element2 = WebDriverWait(wd, 50).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[3]/div[2]/div[4]/div/div[1]/div[1]/div[3]/div[2]/ul/li[9]/a')))
        element2.click()
        time.sleep(0.5)


link_list
wd.current_url