#준비물 : total.html, table.xlsx
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
import pandas as pd
import time
import requests


target_task = 240 # your target task number
jobs = 0
while jobs < target_task:
    jobs = jobs + 1

    driver_path = r'PATH'
    url = "your_cvat_server_url".format(jobs)


    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument(f"webdriver.chrome.driver={driver_path}")
    driver = webdriver.Chrome(options=chrome_options)

    driver.get(url)

    wait = WebDriverWait(driver, 10)
    element = wait.until(EC.presence_of_element_located((By.XPATH, '//div[@class="cvat-login-form-wrapper"]')))
    
    driver.find_element(By.ID, 'credential').send_keys(username) # your username
    driver.find_element(By.ID, 'password').send_keys(password) # your password

    driver.find_element(By.XPATH, '/html/body/div[1]/section/section/main/div/div[2]/div/div/div/form/div[3]/div/div/div/button').click()

    wait.until(EC.url_to_be(url))

    try:
        wait = WebDriverWait(driver, 10)
        element = wait.until(EC.presence_of_element_located((By.XPATH, '//div[@class="ant-col cvat-annotation-header-right-group"]')))
        driver.find_element(By.XPATH, '/html/body/div[1]/section/main/section/header/div/div[3]/button[2]').click()
    except TimeoutException:
        print(f"Element not found for job {jobs}. Continuing to the next job.")
        driver.quit()
        continue

    wait.until(EC.presence_of_element_located((By.XPATH, '//div[@class="ant-table-body"]')))
    
    def get_table_content(driver, xpath):
        table_content = driver.find_element(By.XPATH, xpath).get_attribute('outerHTML')
        return table_content

    def write_to_html(file_path, content):
        with open(file_path, 'a', encoding='utf-8') as file:
            file.write(content)

    xpath = '//div[@class="ant-table-body"]/table/tbody'
    table_content = get_table_content(driver, xpath)

    write_to_html('total.html', table_content)

    driver.quit()

with open('total.html', 'r', encoding='utf-8') as file:
    html_content = file.read()

soup = BeautifulSoup(html_content, 'html.parser')

data = []

for table in soup.find_all('tbody', class_='ant-table-tbody'):
    header = [th.get_text(strip=True) for th in table.find('tr', class_='ant-table-row').find_all('td')]
    
    for row in table.find_all('tr', class_='ant-table-row'):
        data.append([td.get_text(strip=True) for td in row.find_all('td')])

df = pd.DataFrame(data, columns=header)

excel_file_path = 'table.xlsx'
df.to_excel(excel_file_path, index=False)



