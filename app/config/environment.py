import os
import yaml
from dotenv import load_dotenv
load_dotenv()


with open('./config/config.yml', 'r') as file:
    CONFIG = yaml.safe_load(file)

TOKEN = os.environ['TOKEN']
GITLAB_URL = os.environ['GITLAB_URL']
