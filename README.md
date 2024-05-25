# README

## Inspiration
Yesterday, when we were brainstorming problem statement for the hackathon, our team gathered over chips and soda. We were eating and thinking, and amidst our discussion, one of our “health-conscious” teammate was sharing “fascinating” insights about food ingredients and their potential facts and side effects. Many of us were unaware of these intricacies, which sparked an idea to develop a software solution that simplifies access to product-specific health information. (TBH, we were bored to listen him ranting all of the facts ;) 


## What it does
Our software solution provides clear accessible data on the health factors associated with various food items, our software aims to promote healthier lifestyles and dietary habits. It is our first time hackathon and we wanted to have a positive social impact and to foster greater awareness around nutrition and wellness.


## How we built it
Tech Stack: Taipy, Python, OpenCV, Selenium, EasyOCR, Gemini AI, Dynamo DB


## Challenges we ran into
- Food packages are made up of shiny materials, so it gets difficult to capture information using camera, so proper lights are required
- due to shiny packaging, image to text conversion accuracy decreases
- converted text contains lots of misspelled words
- Web scraping posed a challenge due to the different website structures of different products, making generalization difficult.
- Extracted information is unstructured
- it was first time using TaiPy, so learning it from scratch in a day was challenging
- manually created our own database


## Accomplishments that we're proud of
- Able to scan QR code and scrape website for most of the product information
- Image to text conversion for alternate approach to extract ingredients from package with ease
- Used State of the art Gemini AI to summarize result


## What we learned
- Frontend using TaiPy
- Integration of Gemini AI
- Computer Vision using OpenCV and EasyOCR
- Querying on Dynamo DB 


## What's next for SafeBite
- Improve accuracy of Image to text (OCR reading)
- Scale the product to cater different types of food items
- Better Frontend for better visualization
- Increase our Database content

![Flowchart](https://github.com/abhishjain99/SafeBite/blob/main/SafeBite%20Flowchart.png)
