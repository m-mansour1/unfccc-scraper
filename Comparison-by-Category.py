from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import ElementNotInteractableException, NoSuchElementException
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
#from Hashing.HashScrapedData import _hashing
import time
import os
from selenium.webdriver.common.action_chains import ActionChains
import logging
import pandas as pd
import re
from RequestInferSchemaToJsonAPI.main import TriggerInferShemaToJsonAPI

chrome_options = webdriver.ChromeOptions()

# download path
base_path = "\\\\10.30.31.77\data_collection_dump\RawData\Test UNFCCC\Comparison by Category" 
prefs = {'download.default_directory' : base_path}
chrome_options.add_experimental_option('prefs', prefs)
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

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
                            title = driver.find_element(By.XPATH,'/html/body/div/div/div[2]/div/div/div/p').text
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
                            title = title.replace('\\', '').replace('\\\\', '').replace('/',', ').replace('Query results for — ','')
                            title = re.sub(r'[^\w\s-]', '', title.lower())
                            title = re.sub(r'[-\s]+', '-', title).strip('-_')
                            df.to_excel(f'{base_path}\\{title}.xlsx',index = False) 
                            try:
                                BodyDict = {
                                "JobPath":f'//10.30.31.77/data_collection_dump/RawData/Test UNFCCC/Comparison by Category/{title}.xlsx', #* Point to downloaded data for conversion #
                                "JsonDetails":{
                                        ## Required
                                        "organisation": "un-agencies",
                                        "source": "Test UNFCCC",
                                        "source_description" : "The United Nations Framework Convention on Climate Change established an international environmental treaty to combat 'dangerous human interference with the climate system', in part by stabilizing greenhouse gas concentrations in the atmosphere.",
                                        "source_url" : "https://di.unfccc.int",
                                        "table" : title ,
                                        "description" : '' ,
                                        ## Optional
                                        "JobType": "JSON",
                                        "CleanPush": True,
                                        "Server": "str",
                                        "UseJsonFormatForSQL":  False,
                                        "CleanReplace":True,
                                        "MergeSchema": False,
                                        "tags": [
                                                    {"name": ''}
                                                ],
                                        "additional_data_sources": [{      
                                                "name": '',        
                                                "url": ''  ## this object will be ignored if "name" is empty    }
                                        }],
                                        "limitations":'',
                                        "concept":  '',
                                        "periodicity":  '',
                                        "topic": title ,
                                        "created": '',                       #* this should follow the following formats %Y-%m-%dT%H:%M:%S" or "%Y-%m-%d"
                                        "last_modified":'' ,                #* ""               ""                  ""              ""
                                        "TriggerTalend" :  False,    #* initialise to True for production
                                        "SavePathForJsonOutput": "//10.30.31.77/data_collection_dump/TestData/UNFCCC Test/Comparison by Category" #* initialise as empty string for production.
                                    }

                                }
                                # tablenom = BodyDict['JsonDetails']['table']
                                # hashmessage = _hashing(BodyDict['JsonDetails']['source'], tablenom, BodyDict["JobPath"])
                                # if hashmessage["Trigger_InferSchema"] == True and hashmessage["Success"] == True:
                                TriggerInferShemaToJsonAPIClass = TriggerInferShemaToJsonAPI(BodyDict=BodyDict)
                                TriggerInferShemaToJsonAPIClass.TriggerAPI()
                                logging.info(f"Conversion successful - {title} ")
                                print(BodyDict)
                                #     logging.info(f"Conversion successful - {tablenom}, hashmessage: {hashmessage['message']}")
                                # # logging.info(f"Conversion successful for {dataset}")
                                # elif hashmessage['Success'] == True and hashmessage['Trigger_InferSchema'] == False:
                                #     # dont trigger conversion nor talend
                                #     logging.info(f"{hashmessage['message']}")
                                # elif hashmessage['Success'] == False:
                                #     logging.info(f"Hashing error or Unexpected Issue: {hashmessage['message']}")

                            except  Exception as err:
                                print(err)