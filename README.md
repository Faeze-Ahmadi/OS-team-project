# Unsplash Image Scraper

## Overview

This project downloads images from Unsplash, stores them locally, and generates metadata for each image. A summary report is then created in CSV format, detailing the downloaded images.

## Features

- **Image Downloading**: Retrieves images from Unsplash.
- **Metadata Generation**: Creates and saves metadata in JSON files.
- **Summary Report**: Generates a CSV report with image details.
- **Multithreading**: Speeds up the process using concurrent downloads.
- **API Integration**: Uses Phototag API for image keyword generation.

## Quick Start

1. **Clone the Repository**: `git clone https://github.com/your-username/image-downloader.git`
2. **Install Dependencies**: `pip install -r requirements.txt`
3. **Run the Script**: `python main.py`

## Directory Structure

- `images/`: Directory for storing images and metadata.
- `summary_report.csv`: Summary report of the downloaded images.
