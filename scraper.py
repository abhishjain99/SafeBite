from selenium import webdriver
import chromedriver_autoinstaller
import pytesseract
from PIL import Image
import json

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')  # ensure GUI is off
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

chromedriver_autoinstaller.install()
driver = webdriver.Chrome(options=chrome_options)

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import re

# from pyzbar.pyzbar import decode
from PIL import Image
import requests
from bs4 import BeautifulSoup
import easyocr
import cv2


import nltk
from nltk.corpus import words, stopwords
from nltk.tokenize import word_tokenize
from nltk.metrics import edit_distance
import string



import pathlib
import textwrap

import google.generativeai as genai

from IPython.display import display
from IPython.display import Markdown
# from google.colab import userdata

GOOGLE_API_KEY= 'AIzaSyArfTs8tLe-locT_eIdoY5B5z34EHxhZmc'

genai.configure(api_key=GOOGLE_API_KEY)

# # Download NLTK resources
# nltk.download('words')
# nltk.download('punkt')
# nltk.download('stopwords')

# Load English vocabulary and stopwords
english_vocab = set(words.words())
stop_words = set(stopwords.words('english'))
punctuations = set(string.punctuation)


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


def detect_and_fetch_final_urls_opencv(image_path):
    # Load the image
    image = cv2.imread(image_path)

    # Initialize the QRCode detector
    detector = cv2.QRCodeDetector()

    # Detect and decode the QR code
    data, vertices_array, binary_qrcode = detector.detectAndDecode(image)

    # Check if there is a QR code
    if vertices_array is not None:
        print("QR Code detected.")
        intermediate_url = data
        final_url = fetch_final_url_and_extract_link(intermediate_url)
        if final_url:
            return final_url
    else:
        return "No QR code detected in the image."

# Replace the call to the previous function with this one in your main or any other function
# For example:
# url = detect_and_fetch_final_urls_opencv(image_path)



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


def get_ingredients_from_url(binary_img):
    # Example usage
    image_path = 'cocacola1.png'
    # url = detect_and_fetch_final_urls(image_path)
    # url = detect_and_fetch_final_urls_opencv(image_path)
    url = detect_and_fetch_final_urls_opencv(binary_img)
    url += "#ingredients"
    driver.get(url)
    content = driver.find_element(By.XPATH, "/html/body/div/div").text
    print("content------ ", url)
    # pattern = r'Sustainability([\s\S]*?)Please'
    # matches = re.search(pattern, content)
    # result = ''.join(matches.group(1).strip())
    result = content.split("\n")
    return result


def image_to_text(image_path):
    # Open the image
    # with open(image_path, 'rb') as img_file:
    #     # Load image
    #     image = Image.open(img_file)
    #     # Perform OCR
    #     text = pytesseract.image_to_string(image)
    #     return text.strip()
    # Initialize EasyOCR reader
    reader = easyocr.Reader(['en'])

    # Perform OCR
    result = reader.readtext(image_path)

    # Extract text from result
    extracted_text = ' '.join([text[1] for text in result])
    return extracted_text

def get_ingredients_from_image(text):
    pattern = r'INGREDIENTS:(.*)'

    # Search for the pattern in the text
    match = re.search(pattern, text)

    # If a match is found, extract the text after "INGREDIENTS:"
    if match:
        extracted_text = match.group(1).strip()
        print("INGREDIENTS in this product are")
        print(extracted_text)
    else:
        print("Upload product image again")

    return extracted_text


corrected_words = set()
def clean_text(text):
    # food_ingredients = {
    #     "corn", "vegetable", "oil", "canola", "salt", "sugar", "cocoa", "chocolate", "flour", "wheat",
    #     "baking", "soda", "calcium", "phosphate", "lecithin", "artificial", "flavor", "sunflower", "cheddar", "cheese"
    #                                                                                                           "Buttermilk",
    # }
    food_ingredients = {'high-fructose corn syrup',
     'high fructose corn syrup',
     'soybean oil',
     'canola oil',
     'aspartame',
     'saccharin',
     'sucralose',
     'sodium nitrate',
     'monosodium glutamate',
     'butylated hydroxyanisole',
     'butylated hydroxytoluene',
     'artificial colors',
     'artificial sweeteners',
     'artificial flavor',
     'artificial flavors',
     'enriched wheat flour',
     'corn',
     'vegetable Oil',
     'sunflower Oil',
     'corn Oil',
     'maltodextrin (made from corn)',
     'maltodextrin',
     'salt',
     'cheddar cheese',
     'milk',
     "cow's milk",
     "part-skim cow's milk",
     'part-skim cow milk',
     "part skim cow's milk",
     'part skim cow milk',
     'cheese cultures',
     'enzymes',
     'whey',
     'buttermilk',
     'romano cheese',
     'bell pepper powder',
     'disodium inosinate',
     'disodium guanylate',
     'potassium chloride',
     'sodium caseinate',
     'acid',
     'sugar',
     'palm',
     'dextrose',
     'cocoa (processed with alkali)',
     'cocoa',
     'leavening',
     'baking soda',
     'calcium phosphate',
     'soy lecithin',
     'chocolate',
     'unbleached enriched flour (wheat flour)',
     'niacin',
     'reduced iron',
     'thiamine mononitrate vitamin riboflavin vitamin b2%',
     'thiamine mononitrate',
     'riboflavin',
     'folic acid',
     'vegetable oil (soybean and/or canola and/or palm and/or partially hydrogenated cottonseed oil)',
     'soybean',
     '(soybean',
     'and/or canola',
     'canola',
     'and/or palm',
     'and/or partially hydrogenated cottonseed oil)',
     'and/or partially hydrogenated cottonseed oil',
     'partially hydrogenated cottonseed oil',
     'malted barley flour',
     'natural flavor.',
     'natural flavor',
     'natural flavors',
     'milk chocolate',
     'cane sugar',
     'cocoa butter',
     'milk fat',
     'carbonated water',
     'caramel color',
     'phosphoric acid',
     'natural flavors',
     'caffeine'}

    # Tokenize the text into words
    words = nltk.word_tokenize(text.lower())

    # Remove stopwords
    words = [word for word in words if word not in stop_words and word not in punctuations]

    for word in words:
      if word in food_ingredients:
        corrected_words.add(word)
      elif word.lower() == "ingredients" or word.lower == "ingredients:":
        continue
      else:
        closest_word = min(food_ingredients, key=lambda x: edit_distance(word, x))
        corrected_words.add(closest_word)

    # Join the words back into a single string
    cleaned_text = ' '.join(corrected_words)

    return cleaned_text


def to_markdown(text):
  text = text.replace('•', '  *')
  return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))

def genAI(ingredients):
    model = genai.GenerativeModel('gemini-pro')
    query = "Are these ingredients healty for me,", ingredients, "?" , "summarized the version and tell me benefits and drawbacks of them"
    response = model.generate_content(query)
    return response.text

# print(genAI())
image_path = 'cocacola1.png'
# text = image_to_text(image_path)
# result = get_ingredients_from_image(text)

image_path = 'ingred1.jpeg'
extracted_text = image_to_text(image_path)
print("Extracted Text:")
cleaned_text = clean_text(extracted_text)
print("Cleaned Text:")
print(cleaned_text)
ingredients = cleaned_text
print("------- ", ingredients)
json_string = json.dumps(ingredients)
# Converting the string to a list
ingredients_list = json_string.split()

# Preparing the final JSON structure with the list of ingredients
filters_json = {
    "filters": [ingredient.lower() for ingredient in ingredients_list]
}

filters_json
print(filters_json)
response = genAI(ingredients)
print(response)
# url = "http://127.0.0.1:8000/backend/query_dynamodb/"
#
# response = requests.post(url, headers=[], data={'filters': json.dumps(filters_json)})
# print(response.text)


# result = get_ingredients_from_url("qr1.jpeg")
# print(result)

