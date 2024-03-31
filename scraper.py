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

from pyzbar.pyzbar import decode
from PIL import Image
import requests
from bs4 import BeautifulSoup

def fetch_final_url_and_extract_link(intermediate_url):
    try:
        # Send a GET request to the intermediate URL
        response = requests.get(intermediate_url, allow_redirects=False)

        # Check if there is a redirection
        if response.status_code == 301 or response.status_code == 302:
            # Extract the new location from the response headers
            new_location = response.headers['Location']

            # Recursively fetch the final URL using the new location
            return fetch_final_url_and_extract_link(new_location)

        # If there is no redirection, check if the URL is of interest
        if not intermediate_url.startswith("http://smartlabel"):
            # Perform web scraping to extract the link
            soup = BeautifulSoup(response.content, 'html.parser')
            divs = soup.find_all('div', class_='p-1')
            for div in divs:
                link = div.find('a')
                if link:
                    return link['href']

        # Return the final URL
        return intermediate_url
    except requests.exceptions.MissingSchema:
        return None

def detect_and_fetch_final_urls(image_path):
    # Open the image
    with open(image_path, 'rb') as img_file:
        # Load image
        image = Image.open(img_file)
        # Decode QR code
        decoded_objects = decode(image)
        
        if decoded_objects:
            for obj in decoded_objects:
                intermediate_url = obj.data.decode('utf-8')
                final_url = fetch_final_url_and_extract_link(intermediate_url)
                if final_url:
                    return final_url
        else:
            return "No QR code detected in the image."




def get_ingredients_from_url():
  # Example usage
  image_path = 'img_4599.jpg'
  url = detect_and_fetch_final_urls(image_path)
  url+="#ingredients"
  driver.get(url)
  content = driver.find_element(By.XPATH, "/html/body").text
  pattern = r'Sustainability([\s\S]*?)Please'
  matches = re.search(pattern, content)
  result = ''.join(matches.group(1).strip())
  result = result.split("\n")
  return result

result = get_ingredients_from_url()
print(result)