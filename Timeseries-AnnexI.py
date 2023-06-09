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
from RequestInferSchemaToJsonAPI.main import TriggerInferShemaToJsonAPI

chrome_options = webdriver.ChromeOptions()

# download path
base_path = r"\\10.30.31.77\data_collection_dump/RawData/Test UNFCCC/Time Series" 
prefs = {'download.default_directory' : base_path}
chrome_options.add_experimental_option('prefs', prefs)
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

#first page 
driver.get('https://di.unfccc.int/time_series')
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div/div/div[1]/div/div/img')))
soup = BeautifulSoup(driver.page_source, 'html.parser')

select_element = driver.find_element(By.CLASS_NAME,'party-data-filter')
for option in select_element.find_elements(By.TAG_NAME,'option'):
    tag = driver.find_element(By.XPATH,'/html/body/div/div/div[1]/ul/li[1]/a').text
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
    title = title.replace('\\', '').replace('\\\\', '').replace('/',', ').replace('.','').replace(':',' ').replace('₂','2').replace('₆','6').replace('₃','3').replace('₄','4')
    df.to_excel(f'{base_path}\\{title}.xlsx',index = False)
    try:
        BodyDict = {
        "JobPath":f'//10.30.31.77/data_collection_dump/RawData/Test UNFCCC/Time Series/{title}.xlsx', #* Point to downloaded data for conversion #
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
                "SavePathForJsonOutput": "//10.30.31.77/data_collection_dump/TestData/UNFCCC Test/Time Series" #* initialise as empty string for production.
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