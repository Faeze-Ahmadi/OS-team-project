import requests
from bs4 import BeautifulSoup
import os
import json
import threading
import csv

proxies = {
    'http': 'http://127.0.0.1:4392',
    'https': 'https:/127.0.0.1:443'
    }

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

#phototag
url = "https://server.phototag.ai/api/keywords"
def get_tags(SAVE_DIR):
        with open(SAVE_DIR, 'rb') as image:
            headers = {
                "Authorization": f'Bearer 7wdc-dqCn-AkCw-NY317'
            }
            payload = {
                "language": "en",
                "maxKeywords": 5,
                "requiredKeywords": "",
                "customContext": ""
            }
            files = [('file', open('image.jpg',image))]

            response = requests.request("POST",
                                        url,
                                        headers=headers,
                                        data=payload,
                                        files=files)

def generate_summary_report():
    report_path = os.path.join(SAVE_DIR, 'summary_report.csv')
    with open(report_path, 'w', newline='') as csvfile:
        fieldnames = ['image_id', 'photographer', 'category', 'tags', 'description']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for idx in range(len(image_links)):
            image_id = f'image_{idx}'
            metadata_path = os.path.join(SAVE_DIR, image_id + '.json')
            with open(metadata_path, 'r') as file:
                metadata = json.load(file)
            writer.writerow({
                'image_id': metadata.get('image_id', ''),
                'photographer': metadata.get('photographer', ''),
                'category': metadata.get('category', ''),
                'tags': ', '.join(metadata.get('tags', [])),
                'description': metadata.get('description', '')
            })

generate_summary_report()