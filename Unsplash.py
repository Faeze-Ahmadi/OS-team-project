import requests
from bs4 import BeautifulSoup
import os
import json
import threading

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

#threading
def download_and_save_image(link, idx):
    image_id = f'image_{idx}'
    save_path = os.path.join(SAVE_DIR, image_id + '.jpg')
    metadata_path = os.path.join(SAVE_DIR, image_id + '.json')
    
    download_image(link, save_path)
    save_metadata(image_id, "Unknown", "Uncategorized", metadata_path)

threads = []
for idx, link in enumerate(image_links):
    thread = threading.Thread(target=download_and_save_image, args=(link, idx))
    threads.append(thread)
    thread.start()

for thread in threads:
    thread.join()

PHOTOTAG_API_KEY = 'JkUi-5etw-kYo3-afTg-m7'
PHOTOTAG_API_URL = 'https://www.phototag.ai/upload'
def enhance_metadata(image_path):
    with open(image_path, 'rb') as image_file:
        response = requests.post(
            PHOTOTAG_API_URL,
            files={'image': image_file},
            headers={'Authorization': f'Bearer {PHOTOTAG_API_KEY}'}
        )
    return response.json()

def update_metadata(image_id, enhanced_data):
    metadata_path = os.path.join(SAVE_DIR, image_id + '.json')
    with open(metadata_path, 'r') as file:
        metadata = json.load(file)
    metadata.update(enhanced_data)
    with open(metadata_path, 'w') as file:
        json.dump(metadata, file, indent=4)

for idx in range(len(image_links)):
    image_id = f'image_{idx}'
    image_path = os.path.join(SAVE_DIR, image_id + '.jpg')
    enhanced_data = enhance_metadata(image_path)
    update_metadata(image_id, enhanced_data)
