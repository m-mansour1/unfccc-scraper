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
#fifth page part 1
driver.get('https://di.unfccc.int/ghg_profile_annex1')
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div/div/div[1]/div/div/img')))
trs = driver.find_element(By.CLASS_NAME,'dataTable').find_elements(By.TAG_NAME,'tbody')
rows = [each.find_elements(By.XPATH, "tr[@role = 'row']") for each in trs]
for row in rows:
    for each in row:
        tds = each.find_elements(By.TAG_NAME,'td')
        # get topic
        Page_title = tds[0].text
        #get pdf
        download_button = tds[1].find_element(By.TAG_NAME,'a')
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((download_button)))
        webdriver.ActionChains(driver).move_to_element(download_button).click(download_button).perform()
        time.sleep(1)
        def latest_download_file():
            path = base_path
            os.chdir(path)
            files = sorted(os.listdir(os.getcwd()), key=os.path.getmtime)
            newest = files[-1]

            return newest

        fileends = "crdownload"
        while "crdownload" == fileends:
            time.sleep(5) 
            newest_file = latest_download_file()
            if "crdownload" in newest_file:
                fileends = "crdownload"
                # time.sleep(5)
            else:
                fileends = "None"
        latest_download_file()
        file = max([base_path + "\\" + f for f in os.listdir(base_path)],key=os.path.getctime)
        xls = pd.ExcelFile(file)
        sheets = xls.sheet_names
        data_bySector = pd.read_excel(file,sheets[0])
        try:
            ind = data_bySector[data_bySector.columns[0]].index[data_bySector[data_bySector.columns[0]] == 'Average annual change, in percent'].tolist()[0]
            data_bySector = data_bySector[:ind]
        except:
            try:
                ind = data_bySector[data_bySector.columns[0]].index[data_bySector[data_bySector.columns[0]] == 'Average annual changes, in percent'].tolist()[0] 
                data_bySector = data_bySector[:ind]
            except:
                pass
        
        title_sector = Page_title + ' data by Sector ' + data_bySector.columns[0]
        title_sector = title_sector.replace('~$','').replace('~','').replace(':','').replace('/','')
        ind_1 = data_bySector[data_bySector.columns[0]].index[data_bySector[data_bySector.columns[0]] == 'Summary Total'].tolist()[0]
        ind_2 = data_bySector[data_bySector.columns[0]].index[data_bySector[data_bySector.columns[0]] == 'Breakdown by sub-sectors'].tolist()[0]
        df_1 = data_bySector[ind_1+1:ind_2-1]
        title_1 = data_bySector.iloc[ind_1,0] + ' ' + title_sector
        title_1 = title_1.replace('~$','').replace('~','').replace(':','').replace('/','')
        df_1.to_excel(f'{base_path}\\{title_1}.xlsx',index=False)
        df_2 = data_bySector[ind_2+1:]
        title_2 = data_bySector.iloc[ind_2,0] + ' ' + title_sector
        title_2 = title_2.replace('~$','').replace('~','').replace(':','').replace('/','')
        df_2.to_excel(f'{base_path}\\{title_2}.xlsx',index=False)
        data_byGas = pd.read_excel(file,sheets[1])
        try:
            ind = data_byGas[data_byGas.columns[0]].index[data_byGas[data_byGas.columns[0]] == 'Average annual change, in percent'].tolist()[0]
            data_byGas = data_byGas[:ind]
        except:
            try:
                ind = data_byGas[data_byGas.columns[0]].index[data_byGas[data_byGas.columns[0]] == 'Average annual changes, in percent'].tolist()[0]
                data_byGas = data_byGas[:ind]
            except:
                pass
        ind_1 = data_byGas[data_byGas.columns[0]].index[data_byGas[data_byGas.columns[0]] == 'CO₂'].tolist()[0]
        ind_2 = data_byGas[data_byGas.columns[0]].index[data_byGas[data_byGas.columns[0]] == 'CO₂'].tolist()[1]
        title_gas = Page_title + ' data by Gas ' + data_byGas.columns[0]
        title_gas = title_gas.replace('~$','').replace('~','').replace(':','').replace('/','')
        data_byGas[data_byGas.columns[0]][:ind_2-2] = data_byGas.iloc[ind_1-1,0] + '_' + data_byGas[data_byGas.columns[0]][:ind_2-2] .astype(str)
        data_byGas[data_byGas.columns[0]][ind_2:] = data_byGas.iloc[ind_2-1,0] + '_' + data_byGas[data_byGas.columns[0]][ind_2:].astype(str)
        data_byGas = data_byGas.drop(index=[ind_1-1,ind_2-2,ind_2-1])
        data_byGas.to_excel(f'{base_path}\\{title_gas}.xlsx',index=False)
        try:
            summary_data = pd.read_excel(file,sheets[2])
            ind_3 = summary_data[summary_data.columns[3]].index[summary_data[summary_data.columns[3]] == 'Average annual growth rates, in percent per year'].tolist()[0]
            title_3_s = Page_title + ' ' + summary_data.iloc[ind_3,3]
            title_3_s = title_3_s.replace('~$','').replace('~','').replace(':','').replace('/','')
            columns_3 = summary_data.iloc[ind_3+1,]
            columns_3[0] = 'category'
            df_3 = summary_data.iloc[ind_3+2:ind_3+8]
            df_3.columns = columns_3
            df_3 = df_3.dropna(how='all', axis='columns')
            df_3.to_excel(f'{base_path}\\{title_3_s}.xlsx',index=False)
        except:
            pass

#fifth page part 2
driver.get('https://di.unfccc.int/ghg_profile_non_annex1')
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div/div/div[1]/div/div/img')))
trs = driver.find_element(By.CLASS_NAME,'dataTable').find_elements(By.TAG_NAME,'tbody')
rows = [each.find_elements(By.XPATH, "tr[@role = 'row']") for each in trs]
for row in rows:
    for each in row:
        tds = each.find_elements(By.TAG_NAME,'td')
        # get topic
        Page_title = tds[0].text
        #get pdf
        try:
            download_button = tds[1].find_element(By.TAG_NAME,'a')
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((download_button)))
            webdriver.ActionChains(driver).move_to_element(download_button).click(download_button).perform()
        except:
            continue
        time.sleep(1)
        def latest_download_file():
            path = base_path
            os.chdir(path)
            files = sorted(os.listdir(os.getcwd()), key=os.path.getmtime)
            newest = files[-1]

            return newest

        fileends = "crdownload"
        while "crdownload" == fileends:
            time.sleep(5) 
            newest_file = latest_download_file()
            if "crdownload" in newest_file:
                fileends = "crdownload"
                # time.sleep(5)
            else:
                fileends = "None"
        latest_download_file()
        file = max([base_path + "\\" + f for f in os.listdir(base_path)],key=os.path.getctime)
        xls = pd.ExcelFile(file)
        sheets = xls.sheet_names
        data_bySector = pd.read_excel(file,sheets[0])
        try:
            ind = data_bySector[data_bySector.columns[0]].index[data_bySector[data_bySector.columns[0]] == 'Average annual change, in percent'].tolist()[0]
            data_bySector = data_bySector[:ind]
        except:
            try:
                ind = data_bySector[data_bySector.columns[0]].index[data_bySector[data_bySector.columns[0]] == 'Average annual changes, in percent'].tolist()[0] 
                data_bySector = data_bySector[:ind]
            except:
                pass
        
        title_sector = Page_title + ' data by Sector ' + data_bySector.columns[0]
        title_sector = title_sector.replace('~$','').replace('~','').replace(':','').replace('/','')
        ind_1 = data_bySector[data_bySector.columns[0]].index[data_bySector[data_bySector.columns[0]] == 'Summary Total'].tolist()[0]
        ind_2 = data_bySector[data_bySector.columns[0]].index[data_bySector[data_bySector.columns[0]] == 'Breakdown by sub-sectors'].tolist()[0]
        df_1 = data_bySector[ind_1+1:ind_2-1]
        title_1 = data_bySector.iloc[ind_1,0] + ' ' + title_sector
        title_1 = title_1.replace('~$','').replace('~','').replace(':','').replace('/','')
        df_1.to_excel(f'{base_path}\\{title_1}.xlsx',index=False)
        df_2 = data_bySector[ind_2+1:]
        title_2 = data_bySector.iloc[ind_2,0] + ' ' + title_sector
        title_2 = title_2.replace('~$','').replace('~','').replace(':','').replace('/','')
        df_2.to_excel(f'{base_path}\\{title_2}.xlsx',index=False)
        data_byGas = pd.read_excel(file,sheets[1])
        try:
            ind = data_byGas[data_byGas.columns[0]].index[data_byGas[data_byGas.columns[0]] == 'Average annual change, in percent'].tolist()[0]
            data_byGas = data_byGas[:ind]
        except:
            try:
                ind = data_byGas[data_byGas.columns[0]].index[data_byGas[data_byGas.columns[0]] == 'Average annual changes, in percent'].tolist()[0]
                data_byGas = data_byGas[:ind]
            except:
                pass
        ind_1 = data_byGas[data_byGas.columns[0]].index[data_byGas[data_byGas.columns[0]] == 'CO₂'].tolist()[0]
        ind_2 = data_byGas[data_byGas.columns[0]].index[data_byGas[data_byGas.columns[0]] == 'CO₂'].tolist()[1]
        title_gas = Page_title + ' data by Gas ' + data_byGas.columns[0]
        title_gas = title_gas.replace('~$','').replace('~','').replace(':','').replace('/','')
        data_byGas[data_byGas.columns[0]][:ind_2-2] = data_byGas.iloc[ind_1-1,0] + '_' + data_byGas[data_byGas.columns[0]][:ind_2-2] .astype(str)
        data_byGas[data_byGas.columns[0]][ind_2:] = data_byGas.iloc[ind_2-1,0] + '_' + data_byGas[data_byGas.columns[0]][ind_2:].astype(str)
        data_byGas = data_byGas.drop(index=[ind_1-1,ind_2-2,ind_2-1])
        data_byGas.to_excel(f'{base_path}\\{title_gas}.xlsx',index=False)
        try:
            summary_data = pd.read_excel(file,sheets[2])
            ind_3 = summary_data[summary_data.columns[3]].index[summary_data[summary_data.columns[3]] == 'Average annual growth rates, in percent per year'].tolist()[0]
            title_3_s = Page_title + ' ' + summary_data.iloc[ind_3,3]
            title_3_s = title_3_s.replace('~$','').replace('~','').replace(':','').replace('/','')
            columns_3 = summary_data.iloc[ind_3+1,]
            columns_3[0] = 'category'
            df_3 = summary_data.iloc[ind_3+2:ind_3+8]
            df_3.columns = columns_3
            df_3 = df_3.dropna(how='all', axis='columns')
            df_3.to_excel(f'{base_path}\\{title_3_s}.xlsx',index=False)
        except:
            pass

#sixth page
driver.get('https://di.unfccc.int/global_map')
iframeURL = driver.find_element(By.CLASS_NAME, 'global-map').get_attribute("src")

driver.get('https://di.unfccc.int/'+ iframeURL)
options_sector = driver.find_element(By.ID, 'sector').find_elements(By.TAG_NAME,'option')
country1 =[]
value1 = []
country2 =[]
value2 = []
country3 =[]
value3 = []
for option_sector in options_sector:
    option_sector.click()
    options_gas = driver.find_element(By.ID, 'gas').find_elements(By.TAG_NAME,'option')
    for option_gas in options_gas:
        option_gas.click()
        options_year = driver.find_element(By.ID, 'year').find_elements(By.TAG_NAME,'option')
        for option_year in options_year:
            option_year.click()
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'country_list_table')))
            table = driver.find_element(By.ID, 'country_list_table').find_elements(By.TAG_NAME,'tr')
            for row in table:
                country1.append(row.find_elements(By.TAG_NAME,'td')[1].text)
                value1.append(row.find_elements(By.TAG_NAME,'td')[2].text)
                country2.append(row.find_elements(By.TAG_NAME,'td')[5].text)
                value2.append(row.find_elements(By.TAG_NAME,'td')[6].text)
                country3.append(row.find_elements(By.TAG_NAME,'td')[9].text)
                value3.append(row.find_elements(By.TAG_NAME,'td')[10].text)
                
                countryNames = country1 + country2 + country3
                values = value1 + value2 + value3
                df = pd.DataFrame({'Country Name':countryNames,'Value':values})
                df.to_excel(f'{base_path}\\{option_sector.text}_{option_gas.text}_{option_year.text}.xlsx',index=False)

#seventh page part 1
driver.get('https://di.unfccc.int/flex_annex1')
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div/div/div[1]/div/div/img')))

partiesFilter = driver.find_elements(By.CLASS_NAME, "ddlbFilterBox")[0]
driver.execute_script("arguments[0].style.display = 'block';", partiesFilter)
partiesFilter.find_elements(By.CLASS_NAME,'ddlbButton')[0].click()

yearsFilter = driver.find_elements(By.CLASS_NAME, "ddlbFilterBox")[1]
driver.execute_script("arguments[0].style.display = 'block';", yearsFilter)
yearsFilter.find_elements(By.CLASS_NAME,'ddlbButton')[0].click()

categoryFilter = driver.find_elements(By.CLASS_NAME, "ddlbFilterBox")[2]
driver.execute_script("arguments[0].style.display = 'block';", categoryFilter)
category_options = driver.find_element(By.ID,'listboxdiv_categories').find_elements(By.TAG_NAME,'p')


for category_option in category_options:
    if 'not-selectable' in category_option.get_attribute('class'):
        continue
    categoryFilter.find_elements(By.CLASS_NAME,'ddlbButton')[1].click() # deselect all
    category_option.click()
    classificationFilter = driver.find_elements(By.CLASS_NAME, "ddlbFilterBox")[3]
    driver.execute_script("arguments[0].style.display = 'block';", classificationFilter)
    classifications_options = driver.find_element(By.ID,'listboxdiv_classifications').find_elements(By.TAG_NAME,'p')
    for classification_option in classifications_options:
        if 'not-selectable' in classification_option.get_attribute('class'):
            continue
        classificationFilter.find_elements(By.CLASS_NAME,'ddlbButton')[1].click() # deselect all
        classification_option.click()
        valuesFilter = driver.find_elements(By.CLASS_NAME, "ddlbFilterBox")[4]
        driver.execute_script("arguments[0].style.display = 'block';", valuesFilter)
        values_options = driver.find_element(By.ID,'listboxdiv_measures').find_elements(By.TAG_NAME,'p')
        for value_option in values_options:
            if 'not-selectable' in value_option.get_attribute('class'):
                continue
            valuesFilter.find_elements(By.CLASS_NAME,'ddlbButton')[1].click() # deselect all
            value_option.click()
            gasesFilter = driver.find_elements(By.CLASS_NAME, "ddlbFilterBox")[5]
            driver.execute_script("arguments[0].style.display = 'block';", gasesFilter)
            gases_options = driver.find_element(By.ID,'listboxdiv_gases').find_elements(By.TAG_NAME,'p')
            for gas_option in gases_options:
                if 'not-selectable' in gas_option.get_attribute('class'):
                    continue
                gasesFilter.find_elements(By.CLASS_NAME,'ddlbButton')[1].click() # deselect all
                gas_option.click()
                time.sleep(2)
                go_button = driver.find_element(By.CLASS_NAME,'button-group').find_elements(By.TAG_NAME,'button')[0]
                WebDriverWait(driver, 10).until(EC.element_to_be_clickable((go_button)))
                webdriver.ActionChains(driver).move_to_element(go_button).click(go_button).perform()
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'dwhPivot')))
                soup = BeautifulSoup(driver.page_source, 'html.parser')
                table = soup.find(id='dwhPivot')
                title = driver.find_element(By.XPATH,'/html/body/div/div/div[2]/div/div/div[4]/div/div[2]').text
                title = title.replace('\\', '').replace('\\\\', '').replace('/',', ').replace('Query results for — ','')
                title = re.sub(r'[^\w\s-]', '', title.lower())
                title = re.sub(r'[-\s]+', '-', title).strip('-_')
                with open(f'{base_path}\\{title}.csv', 'w', newline='',  encoding="utf-8") as csv_file:
                    writer = csv.writer(csv_file)
                    for row in table.find_all('tr'):
                        csv_row = []
                        for cell in row.find_all(['th', 'td']):
                            csv_row.append(cell.text.strip())
                        writer.writerow(csv_row)

                # show the filter block
                show_button = driver.find_element(By.XPATH,'/html/body/div/div/div[2]/div/div/div[1]/div[2]/div/fieldset/div/div[1]/button[2]')
                WebDriverWait(driver, 10).until(EC.element_to_be_clickable((show_button)))
                webdriver.ActionChains(driver).move_to_element(show_button).click(show_button).perform()

#seventh page part 2
driver.get('https://di.unfccc.int/flex_non_annex1')
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div/div/div[1]/div/div/img')))

partiesFilter = driver.find_elements(By.CLASS_NAME, "ddlbFilterBox")[0]
driver.execute_script("arguments[0].style.display = 'block';", partiesFilter)
partiesFilter.find_elements(By.CLASS_NAME,'ddlbButton')[0].click()

yearsFilter = driver.find_elements(By.CLASS_NAME, "ddlbFilterBox")[1]
driver.execute_script("arguments[0].style.display = 'block';", yearsFilter)
yearsFilter.find_elements(By.CLASS_NAME,'ddlbButton')[0].click()

categoryFilter = driver.find_elements(By.CLASS_NAME, "ddlbFilterBox")[2]
driver.execute_script("arguments[0].style.display = 'block';", categoryFilter)
category_options = driver.find_element(By.ID,'listboxdiv_categories').find_elements(By.TAG_NAME,'p')


for category_option in category_options:
    if 'not-selectable' in category_option.get_attribute('class'):
        continue
    categoryFilter.find_elements(By.CLASS_NAME,'ddlbButton')[1].click() # deselect all
    category_option.click()
    classificationFilter = driver.find_elements(By.CLASS_NAME, "ddlbFilterBox")[3]
    driver.execute_script("arguments[0].style.display = 'block';", classificationFilter)
    classifications_options = driver.find_element(By.ID,'listboxdiv_classifications').find_elements(By.TAG_NAME,'p')
    for classification_option in classifications_options:
        if 'not-selectable' in classification_option.get_attribute('class'):
            continue
        classificationFilter.find_elements(By.CLASS_NAME,'ddlbButton')[1].click() # deselect all
        classification_option.click()
        valuesFilter = driver.find_elements(By.CLASS_NAME, "ddlbFilterBox")[4]
        driver.execute_script("arguments[0].style.display = 'block';", valuesFilter)
        values_options = driver.find_element(By.ID,'listboxdiv_measures').find_elements(By.TAG_NAME,'p')
        for value_option in values_options:
            if 'not-selectable' in value_option.get_attribute('class'):
                continue
            valuesFilter.find_elements(By.CLASS_NAME,'ddlbButton')[1].click() # deselect all
            value_option.click()
            gasesFilter = driver.find_elements(By.CLASS_NAME, "ddlbFilterBox")[5]
            driver.execute_script("arguments[0].style.display = 'block';", gasesFilter)
            gases_options = driver.find_element(By.ID,'listboxdiv_gases').find_elements(By.TAG_NAME,'p')
            for gas_option in gases_options:
                if 'not-selectable' in gas_option.get_attribute('class'):
                    continue
                gasesFilter.find_elements(By.CLASS_NAME,'ddlbButton')[1].click() # deselect all
                gas_option.click()
                time.sleep(2)
                go_button = driver.find_element(By.CLASS_NAME,'button-group').find_elements(By.TAG_NAME,'button')[0]
                WebDriverWait(driver, 10).until(EC.element_to_be_clickable((go_button)))
                webdriver.ActionChains(driver).move_to_element(go_button).click(go_button).perform()
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'dwhPivot')))
                soup = BeautifulSoup(driver.page_source, 'html.parser')
                table = soup.find(id='dwhPivot')
                title = driver.find_element(By.XPATH,'/html/body/div/div/div[2]/div/div/div[4]/div/div[2]').text
                title = title.replace('\\', '').replace('\\\\', '').replace('/',', ').replace('Query results for — ','')
                title = re.sub(r'[^\w\s-]', '', title.lower())
                title = re.sub(r'[-\s]+', '-', title).strip('-_')
                with open(f'{base_path}\\{title}.csv', 'w', newline='',  encoding="utf-8") as csv_file:
                    writer = csv.writer(csv_file)
                    for row in table.find_all('tr'):
                        csv_row = []
                        for cell in row.find_all(['th', 'td']):
                            csv_row.append(cell.text.strip())
                        writer.writerow(csv_row)

                # show the filter block
                show_button = driver.find_element(By.XPATH,'/html/body/div/div/div[2]/div/div/div[1]/div[2]/div/fieldset/div/div[1]/button[2]')
                WebDriverWait(driver, 10).until(EC.element_to_be_clickable((show_button)))
                webdriver.ActionChains(driver).move_to_element(show_button).click(show_button).perform()