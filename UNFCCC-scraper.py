from bs4 import BeautifulSoup
#from Hashing.HashScrapedData import _hashing
import pandas as pd
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.options import Options

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.service import Service as FirefoxService
import time
import os

chrome_options = webdriver.ChromeOptions()

# download path
base_path = "C:\\Users\\10243287\\Desktop\\UNFCCC-scraper\\datasets" 
prefs = {'download.default_directory' : base_path}
chrome_options.add_experimental_option('prefs', prefs)
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

#first page 
driver.get('https://di.unfccc.int/time_series')
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div/div/div[1]/div/div/img')))
soup = BeautifulSoup(driver.page_source, 'html.parser')

select_element = driver.find_element(By.CLASS_NAME,'party-data-filter')
for option in select_element.find_elements(By.TAG_NAME,'option'):
    option.click()
    time.sleep(2)
    # get topic
    title = driver.find_element(By.XPATH,'/html/body/div/div/div[2]/div/div/p').text
    #get table
    table = driver.find_element(By.CLASS_NAME,'react-data-table')
    header = []
    thead = table.find_element(By.TAG_NAME,'thead').find_elements(By.TAG_NAME,'th')
    for th in thead:
        header.append(th.text)
    rows = table.find_elements(By.TAG_NAME,'tr')
    l = []
    for tr in rows[1:]:
        cells = tr.find_elements(By.TAG_NAME,'td')
        cells_text = [cell.text for cell in cells]
        l.append(cells_text)
    df = pd.DataFrame(l,columns=header)
    title = title.replace('\\', '').replace('\\\\', '').replace('/',', ')
    df.to_csv(f'{base_path}\\{title}.csv',index = False)

#second page
driver.get('https://di.unfccc.int/detailed_data_by_party')
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div/div/div[1]/div/div/img')))
soup = BeautifulSoup(driver.page_source, 'html.parser')
select_elements = driver.find_elements(By.CLASS_NAME,'party-data-filter')
#loop through all options
options_countries = select_elements[0].find_elements(By.TAG_NAME,'option')

for option_country in options_countries:
    option_country.click()
    options_years = select_elements[1].find_elements(By.TAG_NAME,'option')
    for option_year in options_years:
        options_Totals = select_elements[2].find_elements(By.TAG_NAME,'option')
        option_year.click()
        for option_Total in options_Totals:
            option_Total.click()
            options_aggregates = select_elements[3].find_elements(By.TAG_NAME,'option')
            for option_aggregate in options_aggregates:
                option_aggregate.click()
                options_equivalents = select_elements[4].find_elements(By.TAG_NAME,'option')
                for option_equivalent in options_equivalents:
                    option_equivalent.click()
                    time.sleep(2)
                    # get topic
                    Page_title = driver.find_element(By.XPATH,'/html/body/div/div/div[2]/div/div/div/p').text
                    try:
                        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, 'dataTable')))
                        table = driver.find_element(By.CLASS_NAME,'dataTable')
                    except:
                        continue
                    header = []
                    thead = table.find_element(By.TAG_NAME,'thead').find_elements(By.TAG_NAME,'th')
                    for th in thead:
                        header.append(th.text)
                    rows = table.find_elements(By.TAG_NAME,'tr')
                    l = []
                    for tr in rows[1:]:
                        cells = tr.find_elements(By.TAG_NAME,'td')
                        cells_text = [cell.text for cell in cells]
                        l.append(cells_text)
                    df = pd.DataFrame(l,columns=header)
                    Page_title = Page_title.replace('\\', '').replace('\\\\', '').replace('/',', ').replace('Query results for — ','')
                    Page_title = re.sub(r'[^\w\s-]', '', Page_title.lower())
                    Page_title = re.sub(r'[-\s]+', '-', Page_title).strip('-_')
                    df.to_csv(f'{base_path}\\{Page_title}.csv',index = False)

#third page
driver.get('https://di.unfccc.int/comparison_by_category')
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div/div/div[1]/div/div/img')))
soup = BeautifulSoup(driver.page_source, 'html.parser')
select_elements = driver.find_elements(By.CLASS_NAME,'party-data-filter')
#loop through all options
options_countries_A = select_elements[0].find_elements(By.TAG_NAME,'option')

for option_country_A in options_countries_A:
    if option_country_A.text == '--Select Party--':
        continue
    option_country_A.click()
    options_countries_B = select_elements[1].find_elements(By.TAG_NAME,'option')
    for option_country_B in options_countries_B:
        if option_country_A.text == option_country_B.text or option_country_B.text == '--Select Party--':
            continue
        options_Totals = select_elements[2].find_elements(By.TAG_NAME,'option')
        option_country_B.click()
        for option_Total in options_Totals:
            option_Total.click()
            options_aggregates = select_elements[3].find_elements(By.TAG_NAME,'option')
            for option_aggregate in options_aggregates:
                option_aggregate.click()
                options_equivalents = select_elements[4].find_elements(By.TAG_NAME,'option')
                for option_equivalent in options_equivalents:
                    option_equivalent.click()
                    options_year_A = select_elements[5].find_elements(By.TAG_NAME,'option')
                    for option_year_A in options_year_A:
                        option_year_A.click()
                        options_year_B = select_elements[6].find_elements(By.TAG_NAME,'option')
                        for option_year_B in options_year_B:
                            if option_year_A.text == option_year_B.text:
                                continue
                            option_year_B.click()
                            time.sleep(1)
                            # get topic
                            Page_title = driver.find_element(By.XPATH,'/html/body/div/div/div[2]/div/div/div/p').text
                            try:
                                WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, 'dataTable')))
                                table = driver.find_element(By.CLASS_NAME,'dataTable')
                            except:
                                continue
                            thead = table.find_element(By.TAG_NAME,'thead').find_elements(By.TAG_NAME,'th')
                            partiesheader = []
                            # for th in thead[:4]:
                            #     partiesheader.append(th.text) #Annex I	, Annex I EIT, Annex I EIT to Annex I Difference
                            # yearsheader = []
                            # for th in thead[4:]:
                            #     yearsheader.append(th.text) #Base year, 1990, Difference, Base year, 1990, Difference, Base year, 1990
                            # for i in range(len(header)):
                            #     header[i] = partiesheader[i] + ' ' + yearsheader[i]
                            #     print(header[i])
                            header = []
                            header = ['Category',
                                        option_country_A.text + ' ' + option_year_A.text,
                                        option_country_A.text + ' ' + option_year_B.text, 'Difference',
                                        option_country_B.text + ' ' + option_year_A.text,
                                        option_country_B.text + ' ' + option_year_B.text, 'Difference',
                                        option_country_B.text + ' to ' + option_country_A.text + ' ' + option_year_A.text,
                                        option_country_B.text + ' to ' + option_country_A.text + ' ' + option_year_B.text]
                            rows = table.find_elements(By.TAG_NAME,'tr')
                            l = []
                            for tr in rows[2:]:
                                cells = tr.find_elements(By.TAG_NAME,'td')
                                cells_text = [cell.text for cell in cells]
                                l.append(cells_text)
                            df = pd.DataFrame(l,columns=header)
                            Page_title = Page_title.replace('\\', '').replace('\\\\', '').replace('/',', ').replace('Query results for — ','')
                            Page_title = re.sub(r'[^\w\s-]', '', Page_title.lower())
                            Page_title = re.sub(r'[-\s]+', '-', Page_title).strip('-_')
                            df.to_csv(f'{base_path}\\{Page_title}.csv',index = False)  

#fourth page
driver.get('https://di.unfccc.int/comparison_by_gas')
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div/div/div[1]/div/div/img')))
soup = BeautifulSoup(driver.page_source, 'html.parser')
select_elements = driver.find_elements(By.CLASS_NAME,'party-data-filter')
#loop through all options
options_countries_A = select_elements[0].find_elements(By.TAG_NAME,'option')

for option_country_A in options_countries_A:
    if option_country_A.text == '--Select Party--':
        continue
    option_country_A.click()
    options_countries_B = select_elements[1].find_elements(By.TAG_NAME,'option')
    for option_country_B in options_countries_B:
        if option_country_A.text == option_country_B.text or option_country_B.text == '--Select Party--':
            continue
        options_categories = select_elements[2].find_elements(By.TAG_NAME,'option')
        option_country_B.click()
        for option_category in options_categories:
            option_category.click()
            options_year_A = select_elements[3].find_elements(By.TAG_NAME,'option')
            for option_year_A in options_year_A:
                option_year_A.click()
                options_year_B = select_elements[4].find_elements(By.TAG_NAME,'option')
                for option_year_B in options_year_B:
                    if option_year_A.text == option_year_B.text:
                        continue
                    option_year_B.click()
                    time.sleep(1)
                    # get topic
                    Page_title = driver.find_element(By.XPATH,'/html/body/div/div/div[2]/div/div/div/p').text
                    try:
                        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, 'dataTable')))
                        table = driver.find_element(By.CLASS_NAME,'dataTable')
                    except:
                        continue
                    thead = table.find_element(By.TAG_NAME,'thead').find_elements(By.TAG_NAME,'th')
                    header = []
                    header = ['Gas',
                                option_country_A.text + ' ' + option_year_A.text,
                                option_country_A.text + ' ' + option_year_B.text, 'Difference',
                                option_country_B.text + ' ' + option_year_A.text,
                                option_country_B.text + ' ' + option_year_B.text, 'Difference',
                                option_country_B.text + ' to ' + option_country_A.text + ' ' + option_year_A.text,
                                option_country_B.text + ' to ' + option_country_A.text + ' ' + option_year_B.text]
                    rows = table.find_elements(By.TAG_NAME,'tr')
                    l = []
                    for tr in rows[2:]:
                        cells = tr.find_elements(By.TAG_NAME,'td')
                        cells_text = [cell.text for cell in cells]
                        l.append(cells_text)
                    df = pd.DataFrame(l,columns=header)
                    Page_title = Page_title.replace('\\', '').replace('\\\\', '').replace('/',', ').replace('Query results for — ','')
                    Page_title = re.sub(r'[^\w\s-]', '', Page_title.lower())
                    Page_title = re.sub(r'[-\s]+', '-', Page_title).strip('-_')
                    df.to_csv(f'{base_path}\\{Page_title}.csv',index = False)   
