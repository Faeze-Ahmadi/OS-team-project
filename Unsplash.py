import requests
from bs4 import BeautifulSoup
import os
import json

UNSPLASH_URL = "https://unsplash.com"
SAVE_DIR = "images"

if not os.path.exists(SAVE_DIR):
    os.makedirs(SAVE_DIR)

def get_image_links():
    response = requests.get(UNSPLASH_URL)
    soup = BeautifulSoup(response.text, 'html.parser')
    links = []
    for img in soup.find_all('img', {'srcset': True}):
        links.append(img['src'])
    return links