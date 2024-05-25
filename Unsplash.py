import requests
from bs4 import BeautifulSoup
import os
import json

UNSPLASH_URL = "https://unsplash.com"
SAVE_DIR = "images"

if not os.path.exists(SAVE_DIR):
    os.makedirs(SAVE_DIR)