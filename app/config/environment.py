import os
from dotenv import load_dotenv
load_dotenv()

TOKEN = os.environ['TOKEN']
GITLAB_URL = os.environ['GITLAB_URL']
LABELS = os.environ.get('LABELS', '').split(',')
