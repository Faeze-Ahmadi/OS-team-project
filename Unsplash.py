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

def get_image_links(UNSPLASH_URL):
    response = requests.get(UNSPLASH_URL)
    soup = BeautifulSoup(response.text, 'html.parser')
    links = []
    for img in soup.find_all('img', {'srcset': True}):
        links.append(img['src'])
    return links[:5]

def download_image(url, save_path):
    response = requests.get(url)
    with open(save_path, 'wb') as file:
        file.write(response.content)

def save_metadata(image_id, photographer, category, save_path , res):
    metadata = json.loads(res)
 
    with open(save_path, 'w') as file:
        json.dump(metadata, file, indent=4)

#phototag
url = "https://server.phototag.ai/api/keywords"
def get_tags(save_path):
        with open(save_path, 'rb') as image:
            headers = {
                "Authorization": f'Bearer ZBcj-H2bE-qmZc-QI8o-FlcO-Phr'
            }
            payload = {
                "language": "en",
                "maxKeywords": 5,
                "requiredKeywords": "beach,sky",
                "customContext": "vacation photo"
            }
            files = [('file', open(save_path,"rb"))]

            response = requests.request("POST",
                                        url,
                                        headers=headers,
                                        data=payload,
                                        files=files)
            print(response.text)
            return response.text

def generate_summary_report(image_links):
    report_path = os.path.join(SAVE_DIR, 'summary_report.csv')
    with open(report_path, 'w', newline='') as csvfile:
        fieldnames = ['image_id' , 'title' , 'description' , 'keywords']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for idx in range(len(image_links)):
            image_id = f'image_{idx}'
            metadata_path = os.path.join(SAVE_DIR, image_id + '.json')
            with open(metadata_path, 'r') as file:
                metadata = json.load(file)
            writer.writerow({
                'image_id': image_id,
                'title': metadata["data"]["title"],
                'description': metadata["data"]["description"],
                'keywords': metadata["data"]["keywords"]
            })

def main():
    image_links = get_image_links(UNSPLASH_URL)

    for idx, link in enumerate(image_links):
        image_id = f'image_{idx}'
        save_path = os.path.join(SAVE_DIR, image_id + '.jpg')
        metadata_path = os.path.join(SAVE_DIR, image_id + '.json')
        
        download_image(link, save_path)
        res = get_tags(save_path)
        save_metadata(image_id, "Unknown", "Uncategorized", metadata_path , res)

    generate_summary_report(image_links)

main()

thread = threading.Thread(target=main)
thread.start()
thread.join()
