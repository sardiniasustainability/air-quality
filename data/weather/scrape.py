from selenium import webdriver
from bs4 import BeautifulSoup as bs4
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from msedge.selenium_tools import EdgeOptions
from msedge.selenium_tools import Edge

# other imports here
edge_options = EdgeOptions()
# if we miss this line, we can't make Edge headless
edge_options.use_chromium = True
# A little different from Chrome cause we don't need two lines before 'headless' and 'disable-gpu'
edge_options.add_argument('headless')
edge_options.add_argument('disable-gpu')
driver = Edge(
    executable_path='C:\\edgedriver_win64\\msedgedriver.exe', options=edge_options)

# navigate to web page
driver.get("https://www.wunderground.com/history/daily/LIEE/date/2021-2-1")

WebDriverWait(driver, 20).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "tr.ng-star-inserted")))

# get page source when element is already present
html = bs4(driver.page_source, 'html.parser')
all_tables = html.body.find_all('tbody')

data_table = all_tables[6]
rows = data_table.find_all('tr', class_="ng-star-inserted")

for row in rows:
    cols = row.find_all('td')
    cols = [ele.text.strip() for ele in cols]
    cols = [ele.replace(u'\xa0', u' ') for ele in cols]
    print(cols)

driver.quit()
