from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

import traceback
import time
import pandas as pd
import requests
from bs4 import BeautifulSoup
from xlwings.constants import TimeUnit

#Start the automation
path = 'C:\Program Files (x86)\chromedriver.exe'
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
while len(wd.current_url) <= len(url):
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
        link_list = []

        soup = BeautifulSoup(page_source, 'lxml')
        links = soup.find_all("div", {"class": "direct-offer-link"})
        for l in links:
            z = l.find('a').get('href')
            link_list.append('https://www.levels.fyi' + z)
            print(l)
    
    #Click next button
        # element2 = WebDriverWait(wd, 50).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.page-next a')))
        time.sleep(0.5)
        element2 = WebDriverWait(wd, 50).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[3]/div[2]/div[4]/div/div[1]/div[1]/div[3]/div[2]/ul/li[9]/a')))
        element2.click()
        time.sleep(0.5)


print(link_list)
wd.current_url

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

'Iterate through links and extract data elements'
import pandas as pd
data = pd.DataFrame()

for url in link_list:
    path = 'C:\Program Files (x86)\chromedriver.exe'
    wd = webdriver.Chrome(path)
    wd.get(url)
    # time.sleep(1)

    'Extract Data Elements'

    company = WebDriverWait(wd, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'company-name'))).text
    level = WebDriverWait(wd, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'level-text'))).text
    job_family = WebDriverWait(wd, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'job-family-text'))).text
    total_comp = WebDriverWait(wd, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'total-average-compensation'))).text
    base_salary = WebDriverWait(wd, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'base-salary-value'))).text
    stock = WebDriverWait(wd, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'stock-salary-value'))).text
    bonus = WebDriverWait(wd, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'bonus-salary-value'))).text
    job_title = WebDriverWait(wd, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'title-text'))).text
    years_exp = WebDriverWait(wd, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'years-of-experience-text'))).text
    years_company = WebDriverWait(wd, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'years-at-company-text'))).text
    years_level = WebDriverWait(wd, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'years-at-level-text'))).text
    location = WebDriverWait(wd, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'location-text'))).text
    work_arrangement = WebDriverWait(wd, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'work-arrangement-text'))).text
    date = WebDriverWait(wd, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'submitted-on'))).text

    'Store Data Elmenents in Dictionary'

    salary_dict = {'company': company, 'level': level, 'job_family': job_family, 'total_comp': total_comp,
                   'base_salary': base_salary, 'stock': stock, 'bonus': bonus, 'years_exp': years_exp,
                   'years_company': years_company, 'years_level': years_level, 'location': location,
                   'work_arrangement': work_arrangement, 'date': date}

    'Append Dictionary to Dataframe'

    data = data.append(salary_dict, ignore_index=True)
    print(data)

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

'URL Formatting to generate all combinations of URLS from location and job title'

unique_urls = []

location_codes = [807,819,501,803,506,602,635,751,825]

job_titles = ['Data%20Scientist', 'Software%20Engineer', 'Product%20Designer', 'Product%20Manager', 'Software%20Engineering%20Manager', 'Technical%20Program%20Manager', 'Solution%20Architect']

for job in job_titles:
    for code in location_codes:
        url = 'https://www.levels.fyi/comp.html?track={}&region={}'.format(job,code)
        unique_urls.append(url)
        print(url)

print(unique_urls)