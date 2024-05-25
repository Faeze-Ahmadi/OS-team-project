# OS team project
# Unsplash Image Scraper

As a preliminary description, we should say that the goal of this project is to develop a Python script to take images from the Unsplash website, categorize and store each image in its own directory and improve metadata through artificial intelligence through PhotoTag.ai. The system generates JSON files for each image detailing the media rating/filing as well as the removal. This project will explore both serial and multithreaded programming approaches along with AI-enhanced metadata generation.

 ------

# Project Process

## Image Scraper from Unsplash

This project is a simple image scraper that downloads images from the Unsplash website and saves them locally.

## Description

The script performs the following tasks:
1. Sends a GET request to the Unsplash homepage.
2. Parses the HTML content of the page to find all image tags with a `srcset` attribute.
3. Extracts the image URLs and stores them in a list.
4. Saves the images to a specified directory on your local machine.

### Code Overview

- `requests`: Used to send HTTP requests to the Unsplash website.
- `BeautifulSoup`: Used to parse HTML content and extract image URLs.
- `os`: Used for directory operations like checking if a directory exists and creating a new directory.
- `json`: Imported for potential future use in saving data in JSON format.

### Usage

1. Define the `UNSPLASH_URL` as the Unsplash homepage URL.
2. Define `SAVE_DIR` as the directory where images will be saved.
3. Create the directory if it does not exist.
4. Define the `get_image_links` function to extract image URLs from the Unsplash homepage.

## Status

This project is currently a work in progress. We are actively working on adding more features and improving the functionality.

