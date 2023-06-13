from bs4 import BeautifulSoup
#from Hashing.HashScrapedData import _hashing
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.options import Options
import openpyxl

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.service import Service as FirefoxService
import time
import re
import os

chrome_options = webdriver.ChromeOptions()

# download path
base_path = "C:\\Users\\10243287\\Desktop\\UNFCCC-scraper\\datasets" 
prefs = {'download.default_directory' : base_path}
chrome_options.add_experimental_option('prefs', prefs)
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

driver.get('https://di.unfccc.int/indicators_annex1')
WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, '/html/body/div/div/div[1]/div/div/img')))

partiesFilter = driver.find_elements(By.CLASS_NAME, "ddlbFilterBox")[0]
driver.execute_script("arguments[0].style.display = 'block';", partiesFilter)
WebDriverWait(driver, 10).until(EC.element_to_be_clickable((partiesFilter.find_elements(By.CLASS_NAME,'ddlbButton')[0])))
partiesFilter.find_elements(By.CLASS_NAME,'ddlbButton')[0].click()

yearsFilter = driver.find_elements(By.CLASS_NAME, "ddlbFilterBox")[1]
driver.execute_script("arguments[0].style.display = 'block';", yearsFilter)
WebDriverWait(driver, 10).until(EC.element_to_be_clickable((yearsFilter.find_elements(By.CLASS_NAME,'ddlbButton')[0])))
yearsFilter.find_elements(By.CLASS_NAME,'ddlbButton')[0].click()

filters = driver.find_elements(By.CLASS_NAME,'indicator-box')

#initial 
NumParametersRadio = False
DenParametersRadio = True

def executeFilter(NumParametersRadio, DenParametersRadio):
    options_Filter1 = filters[1].find_elements(By.CLASS_NAME,'ddlbFilterBox')
    options1 = options_Filter1[0].find_elements(By.TAG_NAME,'p')
    driver.execute_script("arguments[0].style.display = 'block';", options_Filter1[0])
    for option1 in options1[1:]:
        if 'not-selectable' in option1.get_attribute('class'):
            continue
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((option1)))
        driver.execute_script("arguments[0].click()", option1)
        driver.execute_script("arguments[0].style.display = 'block';", options_Filter1[0])
        time.sleep(1)
        options2 = options_Filter1[1].find_elements(By.TAG_NAME,'p')
        driver.execute_script("arguments[0].style.display = 'block';", options_Filter1[1])
        for option2 in options2[1:]:
            if 'not-selectable' in option2.get_attribute('class'):
                continue
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((option2)))
            driver.execute_script("arguments[0].click()", option2)
            driver.execute_script("arguments[0].style.display = 'block';", options_Filter1[1])
            time.sleep(1)
            options3 = options_Filter1[2].find_elements(By.TAG_NAME,'p')
            driver.execute_script("arguments[0].style.display = 'block';", options_Filter1[2])
            for option3 in options3[1:]:
                if 'not-selectable' in option3.get_attribute('class'):
                    continue
                WebDriverWait(driver, 10).until(EC.element_to_be_clickable((option3)))
                driver.execute_script("arguments[0].click()", option3)
                driver.execute_script("arguments[0].style.display = 'block';", options_Filter1[2])
                time.sleep(1)
                options4 = options_Filter1[3].find_elements(By.TAG_NAME,'p')
                driver.execute_script("arguments[0].style.display = 'block';", options_Filter1[3])
                for option4 in options4[1:]:
                    if 'not-selectable' in option4.get_attribute('class'):
                        continue
                    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((option4)))
                    driver.execute_script("arguments[0].click()", option4)
                    driver.execute_script("arguments[0].style.display = 'block';", options_Filter1[3])
                    time.sleep(1)
                    if NumParametersRadio:
                        options5 = options_Filter1[4].find_elements(By.TAG_NAME,'p')
                        driver.execute_script("arguments[0].style.display = 'block';", options_Filter1[4])
                        for option5 in options5:
                            if 'not-selectable' in option5.get_attribute('class'):
                                continue
                            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((option5)))
                            driver.execute_script("arguments[0].click()", option5)
                            driver.execute_script("arguments[0].style.display = 'block';", options_Filter1[4])
                            time.sleep(1)

                    #second filter
                    options_Filter2 = filters[2].find_elements(By.CLASS_NAME,'ddlbFilterBox')
                    options6 = options_Filter2[0].find_elements(By.TAG_NAME,'p')
                    driver.execute_script("arguments[0].style.display = 'block';", options_Filter2[0])
                    for option6 in options6[1:]:
                        if 'not-selectable' in option6.get_attribute('class') or 'disabled' in option6.get_attribute('class'):
                            continue
                        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((option6)))
                        driver.execute_script("arguments[0].click()", option6)
                        driver.execute_script("arguments[0].style.display = 'block';", options_Filter2[0])
                        time.sleep(1)
                        options7 = options_Filter2[1].find_elements(By.TAG_NAME,'p')
                        driver.execute_script("arguments[0].style.display = 'block';", options_Filter2[1])
                        for option7 in options7[1:]:
                            if 'not-selectable' in option7.get_attribute('class'):
                                continue
                            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((option7)))
                            driver.execute_script("arguments[0].click()", option7)
                            driver.execute_script("arguments[0].style.display = 'block';", options_Filter2[1])
                            time.sleep(1)
                            options8 = options_Filter2[2].find_elements(By.TAG_NAME,'p')
                            driver.execute_script("arguments[0].style.display = 'block';", options_Filter2[2])
                            for option8 in options8[1:]:
                                if 'not-selectable' in option8.get_attribute('class'):
                                    continue
                                WebDriverWait(driver, 10).until(EC.element_to_be_clickable((option8)))
                                driver.execute_script("arguments[0].click()", option8)
                                driver.execute_script("arguments[0].style.display = 'block';", options_Filter2[2])
                                time.sleep(1)
                                options9 = options_Filter2[3].find_elements(By.TAG_NAME,'p')
                                driver.execute_script("arguments[0].style.display = 'block';", options_Filter2[3])
                                for option9 in options9[1:]:
                                    if 'not-selectable' in option9.get_attribute('class'):
                                        continue
                                    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((option9)))
                                    driver.execute_script("arguments[0].click()", option9)
                                    driver.execute_script("arguments[0].style.display = 'block';", options_Filter2[3])
                                    time.sleep(1)
                                    if DenParametersRadio:
                                        options10 = options_Filter2[4].find_elements(By.TAG_NAME,'p')
                                        driver.execute_script("arguments[0].style.display = 'block';", options_Filter2[4])
                                        for option10 in options10[1:]:
                                            if 'not-selectable' in option10.get_attribute('class'):
                                                continue
                                            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((option10)))
                                            driver.execute_script("arguments[0].click()", option10)
                                            driver.execute_script("arguments[0].style.display = 'block';", options_Filter2[4])
                                            time.sleep(1)


                                            # saving the data 
                                            
                                            #table = driver.find_element(By.CLASS_NAME,'dataTable')
                                            #data = driver.find_element(By.ID,'DataTables_Table_0').find_element(By.TAG_NAME,'tbody')
                                            title = driver.find_element(By.XPATH,'/html/body/div/div/div[2]/div/div/div[4]/div[1]/table/tbody/tr[2]/td[2]').text +' '+ driver.find_element(By.XPATH, '/html/body/div/div/div[2]/div/div/div[4]/div[1]/table/tbody/tr[3]/td[2]').text
                                            title = title.replace('\\', '').replace('\\\\', '').replace('/',', ').replace('Query results for — ','').replace('Category: ', '').replace('Classification:', '')
                                            title = title.replace('Unit:', '').replace('Measure:', '').replace('Gas:','')
                                            soup = BeautifulSoup(driver.page_source, "html.parser")

                                            table = soup.find(class_='dataTable')
                                            datatable = soup.find(id='DataTables_Table_0')

                                            columns = [i.get_text(strip=True) for i in table.find_all("th")]
                                            data = []

                                            for tr in datatable.find("tbody").find_all("tr"):
                                                data.append([td.get_text(strip=True) for td in tr.find_all("td")])

                                            df = pd.DataFrame(data, columns=columns)

                                            df.to_excel(f'{base_path}\\{title}.xlsx', index=False)
                                    if not DenParametersRadio:
                                        title = driver.find_element(By.XPATH,'/html/body/div/div/div[2]/div/div/div[4]/div[1]/table/tbody/tr[2]/td[2]').text +' '+ driver.find_element(By.XPATH, '/html/body/div/div/div[2]/div/div/div[4]/div[1]/table/tbody/tr[3]/td[2]').text
                                        title = title.replace('\\', '').replace('\\\\', '').replace('/',', ').replace('Query results for — ','').replace('Category: ', '').replace('Classification:', '')
                                        title = title.replace('Unit:', '').replace('Measure:', '').replace('Gas:','').replace('(Numerator)', '').replace('(Denominator)', '').strip()
                                        soup = BeautifulSoup(driver.page_source, "html.parser")

                                        table = soup.find(class_='dataTable')
                                        datatable = soup.find(id='DataTables_Table_0')

                                        columns = [i.get_text(strip=True) for i in table.find_all("th")]
                                        data = []

                                        for tr in datatable.find("tbody").find_all("tr"):
                                            data.append([td.get_text(strip=True) for td in tr.find_all("td")])

                                        df = pd.DataFrame(data, columns=columns)

                                        df.to_excel(f'{base_path}\\{title}.xlsx', index=False)

#execute the first filter
def NumeratorEmission():
    radio = filters[1].find_elements(By.CLASS_NAME,'radio')[0].find_element(By.TAG_NAME, 'input')
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((radio)))
    driver.execute_script("arguments[0].click()", radio)

def DenominatorEmission():
    radio = filters[2].find_elements(By.CLASS_NAME,'radio')[0].find_element(By.TAG_NAME, 'input')
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((radio)))
    driver.execute_script("arguments[0].click()", radio)

def NumeratorParameters():
    radio = filters[1].find_elements(By.CLASS_NAME,'radio')[1].find_element(By.TAG_NAME, 'input')
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((radio)))
    driver.execute_script("arguments[0].click()", radio)

def DenominatorParameters(): 
    radio = filters[2].find_elements(By.CLASS_NAME,'radio')[1].find_element(By.TAG_NAME, 'input')
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((radio)))
    driver.execute_script("arguments[0].click()", radio)

def execute():
    NumeratorEmission()
    DenominatorParameters()
    NumParametersRadio = False
    DenParametersRadio = True
    executeFilter(NumParametersRadio, DenParametersRadio)
    time.sleep(2)

    NumeratorEmission()
    DenominatorEmission()
    NumParametersRadio = False
    DenParametersRadio = False
    executeFilter(NumParametersRadio, DenParametersRadio)
    time.sleep(2)

    NumeratorParameters()
    DenominatorEmission()
    NumParametersRadio = True
    DenParametersRadio = False
    executeFilter(NumParametersRadio, DenParametersRadio)
    time.sleep(2)

    NumeratorParameters()
    DenominatorParameters()
    NumParametersRadio = True
    DenParametersRadio = True
    executeFilter(NumParametersRadio, DenParametersRadio)
    time.sleep(2)
    
execute()
