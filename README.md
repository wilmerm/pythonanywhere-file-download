# pythonanywhere_file_download
Simple Python script for download files from PythonAnywhere

## Requirements

- Python 3.x
- `requests` library
- `python-dotenv` library

## Instalation

```.sh
python3 -m venv .env
```
```.sh
source .env/bin/activate
```
```.sh
pip install -r requirements.txt
```

## Configuration

Create a `.env` file in the same directory as the script and define the following environment variables:

```.env
USERNAME=your_pythonanywhere_username
TOKEN=your_pythonanywhere_token_authentication
API_URL=https://www.pythonanywhere.com/api/v0/user/{username}/
```

## Use

Run the script by supplying the following command line arguments:

```.sh
python main.py <remote_dir> <local_dir>
```

### Example

```.sh
python main.py /home/myremoteusername/backups /home/mylocalusername/backups
```

## Notes

[The PythonAnywhere API](https://help.pythonanywhere.com/pages/API)



