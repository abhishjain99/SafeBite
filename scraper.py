from selenium import webdriver
import chromedriver_autoinstaller

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless') # ensure GUI is off
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

chromedriver_autoinstaller.install()
driver = webdriver.Chrome(options=chrome_options)

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import re

def get_ingredients_from_url():
  url = "https://menu.pepsico.info/b5111082-25dd-401c-b801-690cba7ed711/index.html?cname=00028400048026_30056300_SunChips_BR&scantime=2024-03-30T20%3A07%3A17Z&utm_source=scanbuy&utm_campaign=smartlabel_scan&utm_medium=qrcode"
  driver.get(url)

  if not url.find("smartlabel"):
    url = [my_elem.get_attribute("href") for my_elem in WebDriverWait(driver, 20).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "div[class='p-1'] > a[href]")))][0]
    url = url + "#ingredients"
  else:
    url = 'https://smartlabel.mondelez.info/044000020170-0002-en-US/index.html?scantime=2024-03-30T19%3A25%3A07Z&utm_source=scanbuy&utm_campaign=smartlabel_scan&utm_medium=qrcode#ingredients'
  driver.get(url)

  content = driver.find_element(By.XPATH, "/html/body").text

  pattern = re.compile(r'(?<=Brand & Sustainability\n)(.*?)(?=Please refer)', re.DOTALL)
  matches = re.findall(pattern, content)
  result = ''.join(matches)
  result = re.sub(r'\bAND/OR \b', '', result)
  result = result.split("\n")
  return result

result = get_ingredients_from_url()
print(result)
