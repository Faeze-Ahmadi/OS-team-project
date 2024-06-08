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

def download_image(url, save_path):
    response = requests.get(url)
    with open(save_path, 'wb') as file:
        file.write(response.content)

def save_metadata(image_id, photographer, category, save_path):
    metadata = {
        'image_id': image_id,
        'photographer': photographer,
        'category': category
    }
    with open(save_path, 'w') as file:
        json.dump(metadata, file, indent=4)

image_links = get_image_links()

for idx, link in enumerate(image_links):
    image_id = f'image_{idx}'
    save_path = os.path.join(SAVE_DIR, image_id + '.jpg')
    metadata_path = os.path.join(SAVE_DIR, image_id + '.json')
    
    download_image(link, save_path)
    save_metadata(image_id, "Unknown", "Uncategorized", metadata_path)