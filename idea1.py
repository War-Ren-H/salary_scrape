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

import math

#Start the automation
path = r"C:\Users\Statistician X\Downloads\chromedriver_win32\chromedriver.exe"
options = Options()
#options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

wd = webdriver.Chrome(path, chrome_options = options)
#wd = webdriver.Safari()
url = 'https://www.levels.fyi/comp.html?track=Data%20Scientist&region=803'
wd.get(url)

element = WebDriverWait(wd,10).until(EC.presence_of_element_located((By.CLASS_NAME,'dropdown')))
element.click()
time.sleep(0.2)
element = WebDriverWait(wd,10).until(EC.presence_of_element_located((By.XPATH,'/html/body/div[3]/div[2]/div[4]/div/div[1]/div[1]/div[3]/div[1]/span[2]/span/ul/li[4]')))
element.click()
time.sleep(0.2)

link_list = []

#Counter for how many times next page has been clicked in case the program messes up
page_next = 0

#Figure out how many pages there are
this_page = wd.page_source
this_soup = BeautifulSoup(this_page, 'lxml')
this_info = this_soup.find('span', {"class": "pagination-info"})
total_entries = [int(s) for s in this_info.text.split() if s.isdigit()][2]
num_pages = math.ceil(total_entries/100)
print("num_pages: " + str(num_pages))


for i in range(num_pages):
    #Find the number of tabs on each page
    this_page = wd.page_source
    this_soup = BeautifulSoup(this_page, 'lxml')
    this_info = this_soup.find('span', {"class": "pagination-info"})
    this_info2 = this_soup.find('div', {"class": "anonymization-hidden-disclaimer lfont"})
    entries_and_rows = [int(s) for s in this_info.text.split() if s.isdigit()]
    #If no entries on the page are anonymous, automatically set to 0 to avoid error.
    if this_info2 is None:
        anon = 0
    else:
        anon = [str(s) for s in this_info2.text.split() if s.isdigit()][0:2]
        anon_nums = int("".join(anon))
    num_tabs = (entries_and_rows[1] - entries_and_rows[0] + 1 - anon_nums)
    print("anon: " + str(anon_nums))
    print("num_tabs: " + str(num_tabs))

    #Open all of the tabs
    for j in range(1,num_tabs*2,2):
        try:
            xpath = '//*[@id="compTable"]/tbody/tr[{}]'.format(str(j))
            element = WebDriverWait(wd, 50).until(EC.presence_of_element_located((By.XPATH, xpath)))
            element.click()
            time.sleep(0.01)
            print("detail: ", j)
        except:
            #get_back_to_work()
            pass

#Extract the relevant links and append to link_list
    page_source = wd.page_source

    soup = BeautifulSoup(page_source, 'lxml')
    links = soup.find_all("div", {"class": "direct-offer-link"})
    for l in links:
        z = l.find('a').get('href')
        link_list.append('https://www.levels.fyi' + z)
        print(l)

#Click next button
    if i < num_pages - 1:
        # element2 = WebDriverWait(wd, 50).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.page-next a')))
        time.sleep(0.5)
        #Page next tag is dynamic based on how many pages there are. This accounts for URLs with fewer observations.
        tag = '/html/body/div[3]/div[2]/div[4]/div/div[1]/div[1]/div[3]/div[2]/ul/li[{}]/a'.format(min(num_pages+2, 9))
        element2 = WebDriverWait(wd, 50).until(EC.presence_of_element_located((By.XPATH, tag)))
        element2.click()
        time.sleep(0.5)
        page_next += 1
    else:
        #At the last page, reset page_next for the next URL
        print("Huzzah!")
        page_next = 0


print(link_list)

link_list2 = link_list[:50]
#wd.current_url

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

'Iterate through links and extract data elements'
import pandas as pd
data = pd.DataFrame()

start = time.time()
for url in link_list2:
    try:
        #path = 'C:\Program Files (x86)\chromedriver.exe'
        wd = webdriver.Chrome(path)
        wd.get(url)
        time.sleep(1)
        page = wd.page_source
        soup = BeautifulSoup(page, 'lxml')

        'Extract Data Elements'
        company = soup.find("h3", {"class": "company-name"}).text
        #level can sometimes be "None"
        level = soup.find("h3", {"class":"level-text"})
        if level is None:
            level = ''
        else:
            level = level.text
        job_family = soup.find("h3", {"class":"job-family-text"}).text
        #total_comp displays the wrong value. Removed it from the dictionary
        #total_comp = soup.find("span", {"class": "total-average-compensation"}).text
        base_salary = soup.find("p", {"class":"base-salary-value"}).text
        stock = soup.find("p", {"class":"stock-salary-value"}).text
        bonus = soup.find("p", {"class":"bonus-salary-value"}).text
        job_title = soup.find("span", {"class":"title-text"}).text
        years_exp = soup.find("span", {"class":"years-of-experience-text"}).text
        years_company = soup.find("span", {"class":"years-at-company-text"}).text
        years_level = soup.find("span", {"class":"years-at-level-text"}).text
        location = soup.find("p", {"class":"location-text"}).text
        work_arrangement = soup.find("p", {"class":"work-arrangement-text"}).text
        perspective = soup.find("p", {"class":"comp-perspective-text"}).text
        date = soup.find("p", {"class":"submitted-on"}).text
        education = soup.find("p", {"class":"education-text"})
        if education is None:
            education = ''
        else:
            education = education.text
        gender = soup.find("p", {"class":"gender-text"})
        if gender is None:
            gender = ''
        else:
            gender = gender.text
        ethnicity = soup.find("p", {"class":"ethnicity-text"})
        if ethnicity is None:
            ethnicity = ''
        else:
            ethnicity = ethnicity.text
        focus = soup.find("p", {"class":"focus-tag-text"})
        if focus is None:
            focus = ''
        else:
            focus = focus.text

        'Store Data Elmenents in Dictionary'

        salary_dict = {'company': company, 'level': level, 'job_family': job_family, 'job_title': job_title,
                       'perspective': perspective, 'education': education, 'gender': gender, 'ethnicity': ethnicity,
                       'base_salary': base_salary, 'stock': stock, 'bonus': bonus, 'years_exp': years_exp,
                       'years_company': years_company, 'years_level': years_level, 'location': location,
                       'focus_tag': focus, 'work_arrangement': work_arrangement, 'date': date}

        'Append Dictionary to Dataframe'

        data = data.append(salary_dict, ignore_index=True)
        print(data)

    except:
        pass

print("Total time to run beautiful soup version = " + str(time.time() - start))
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
