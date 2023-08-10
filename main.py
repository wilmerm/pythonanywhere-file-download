import sys
import os
from typing import Dict
from pathlib import Path

import requests
from dotenv import load_dotenv


load_dotenv()

username = os.getenv('USERNAME')
token = os.getenv('TOKEN')
headers = {'Authorization': f'Token {token}'}
api_url = os.getenv('API_URL').format(username=username)


def get_path_url(path):
    return f'{api_url}files/path{path}'


def list_dir(path) -> Dict[str, Dict[str, str]]:
    """Gets a dictionary with information about the files in the directory.

    Args:
        path (str): The remote path to the directory to be listed.

    Returns:
        Dict: A dictionary containing information about files and directories.
        {
            'filename': {
                'type': 'file' | 'directory',
                'url': 'file or directory URL'
            }
        }
    """
    url = get_path_url(path)
    res = requests.get(url, headers=headers)

    if res.status_code == 200:
        return res.json()
    raise ValueError(f'Got unexpected status code: {res.status_code}, URL: {res.url}, reason: {res.reason}')


def download_file(url, local_filename):
    try:
        with requests.get(url, stream=True, headers=headers) as res:
            res.raise_for_status() # Check if response is ok

            total_size = int(res.headers.get('content-length', 0))
            bytes_downloaded = 0

            with open(local_filename, 'wb') as file:
                for chunk in res.iter_content(chunk_size=8192):
                    file.write(chunk)
                    bytes_downloaded += len(chunk)
                    progress = (bytes_downloaded / total_size) * 100
                    print(f"Downloaded: {bytes_downloaded}/{total_size} bytes. Progress: {progress:.2f}%", end='\r')
    except requests.exceptions.RequestException as e:
        print(f'Error downloading the file: {e}')
        return False
    print(f'{local_filename} is Ok.')
    return True


def download_dir(remote_dir, local_dir):
    files_dict = list_dir(remote_dir)

    for filename in files_dict:
        file_type = files_dict[filename]['type']
        file_url = files_dict[filename]['url']
        remote_path = os.path.join(remote_dir, filename)
        print(f'{file_type}: {remote_path}')

        if file_type== 'file':
            local_filename = os.path.join(local_dir, filename)
            download_file(file_url, local_filename)
        elif file_type == 'directory':
            remote_dir_2 = os.path.join(remote_dir, filename)
            local_dir_2 = os.path.join(local_dir, filename)

            if not os.path.exists(local_dir_2):
                os.makedirs(local_dir_2)

            download_dir(remote_dir_2, local_dir_2)


def main():
    if len(sys.argv) < 3:
        print('Use: python main.py <remote_dir> <local_dir>')
        return 1
    remote_dir = sys.argv[1]
    local_dir = sys.argv[2]
    download_dir(remote_dir, local_dir)


if __name__ == '__main__':
    sys.exit(main())
