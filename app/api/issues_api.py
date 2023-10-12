import threading
from flask import request, Response
import app.core.issues as issues
from flask import Blueprint

bp = Blueprint('issues', __name__, url_prefix='/issue')


@bp.route("/full-scan", methods=['POST'])
def full_scan():
    response = Response('Running full scan')
    threading.Thread(target=issues.process_all_issues).start()
    return response


@bp.route("/webhook", methods=['POST'])
def webhook_issue():
    response = Response('Running issue webhook')
    threading.Thread(target=issues.process_issue, args=(
        request.json['project'], request.json['object_attributes']['iid'],)).start()

    return response
