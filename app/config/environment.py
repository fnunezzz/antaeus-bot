import os
from dotenv import load_dotenv
load_dotenv()

TOKEN = os.environ['TOKEN']
GITLAB_URL = os.environ['GITLAB_URL']
OLD_ISSUE_TIME_DELTA = int(os.environ.get('OLD_ISSUE_TIME_DELTA', 10))
OLD_ISSUE_OLD_LABELS = os.environ.get('OLD_ISSUE_OLD_LABELS', '').split(',')
OLD_ISSUE_NEW_LABELS = os.environ.get('OLD_ISSUE_NEW_LABELS', '').split(',')
LABELS = os.environ.get('LABELS', '').split(',')
