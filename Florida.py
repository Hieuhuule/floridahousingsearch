from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import pandas as pd
import time
from datetime import datetime

options = webdriver.ChromeOptions()
options.add_argument("--log-level=3")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
options.add_argument('--disable-blink-features=AutomationControlled')

webdriver_path = ChromeDriverManager().install()

driver = webdriver.Chrome(service=webdriver.chrome.service.Service(ChromeDriverManager().install()), options=options)


driver.maximize_window()

listofdict = list()
# Change the below link
Link ='https://www.myhousingsearch.com/dbh/SearchHousingSubmit.html?city_id=35857&ch=FL&type=rental&text_search=Tampa'

driver.get(Link)
time.sleep(4)
try:
    Cookies = driver.find_element(By.XPATH,'//*[@id="closebtn"]')
    Cookies.click()
    time.sleep(5)
except:
    pass

for i in range(1,1000):
    try:
        Results = driver.find_elements(By.XPATH,'//div[@class="shsAddress"]')
        for data in Results:
            datadict = dict()
            URL = data.find_element(By.XPATH,'.//a').get_attribute('href')
            parent = driver.window_handles[0]
            driver.execute_script(f'''window.open("{URL}","_blank");''')
            chld = driver.window_handles[1]
            driver.switch_to.window(chld)
            time.sleep(2)

            datadict['Main URL'] = URL
            try:
                datadict['Address'] = driver.find_element(By.XPATH,'//div[@class="vuAddress"]').text.replace('\n',' ')
            except:
                datadict['Address'] = ""

            Table= driver.find_elements(By.XPATH,'//div[@class="vuContact"]/table[@class="tabularDetails"]/tbody/tr')

            for Entry in Table:
                try:
                    Attribute = Entry.find_element(By.XPATH,'.//td[@class="tbL"]').text
                    datadict[Attribute] = Entry.find_element(By.XPATH,'.//td[@class="tbC"]').text
                except:
                    pass

            print(datadict)
            listofdict.append(datadict)
            driver.close()
            driver.switch_to.window(parent)

        Next_Page = driver.find_element(By.XPATH,'//a[@title="next10 properties"]')
        Next_Page.click()
        time.sleep(5)
    
    except:
        break

df = pd.DataFrame.from_dict(listofdict)
now = datetime.now()
current_date = now.strftime("%d_%m_%Y_%H_%M")
df.to_csv(f'New_File{current_date}.csv', index=False)
print('Data Saved in CSV!')

driver.quit()
