import os
import yaml
from dotenv import load_dotenv
load_dotenv()

PATH = os.environ['CONFIG_PATH']

with open(PATH, 'r') as file:
    CONFIG = yaml.safe_load(file)

print(CONFIG)

TOKEN = os.environ['TOKEN']
GITLAB_URL = os.environ['GITLAB_URL']
