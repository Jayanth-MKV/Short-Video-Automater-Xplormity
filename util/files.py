import os
import json
import logging

import requests
from .const import LOG_PATH

# Configure logging
# logging.basicConfig(filename=LOG_PATH, level=logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s')


def create_directories(isCreated):

    if not isCreated:
        # Ensure that the required directories exist, if not, create them
        directories = [LOG_PATH]
        for directory in directories:
            if not os.path.exists(directory):
                os.makedirs(directory)
                logging.info(f"Created directory: {directory}")
            else:  
                logging.info(f"directory exists: {directory}")
    else:
        logging.info("Directory creation skipped as per configuration.")


def make_dir(directory:str):
    if not os.path.exists(directory):
        os.makedirs(directory)
        logging.info(f"Created directory: {directory}")
    else:  
        logging.info(f"directory exists: {directory}")

def load_json(file_path: str):
    with open(file_path, 'r') as f:
        data = json.load(f)
    return data

def save_json(file_path: str, data: list|dict):
    with open(f"{file_path}",'w') as f:
        f.write(f'{{"result":{json.dumps(data)}}}')

def save_metajson(file_path: str, data: dict):
    with open(f"{file_path}",'w') as f:
        f.write(f'{json.dumps(data)}')

def save_txt(file_path: str, data: str):
    with open(f"{file_path}",'w') as f:
        f.write(data)

def load_txt(file_path: str):
    with open(f"{file_path}",'r') as f:
        data = f.read()
    return data

def save_video(logger,video_url, file_path):
    dir_path = "/".join(file_path.split("/")[:-1])
    os.makedirs(dir_path, exist_ok=True)

    # file_name = os.path.basename(video_url)
    # file_path = os.path.join(dir_path, file_name)

    if os.path.exists(file_path):
        logger.info(f"File already exists: {file_path}")
        return
    
    response = requests.get(video_url, stream=True)

    if response.status_code == 200:
        with open(file_path, "wb") as file:
            # Iterate over the response data in chunks and write to the file
            for chunk in response.iter_content(chunk_size=1024):
                file.write(chunk)
            
        logger.info(f"Video saved successfully to: {file_path}")
    else:
        logger.error(f"Failed to download the video from: {video_url}")