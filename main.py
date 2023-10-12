
from flask import Flask
from app.core.gitlab import auth
from app.api.issues_api import bp as issue_bp

app = Flask(__name__)
app.register_blueprint(issue_bp)

if __name__ == '__main__':
    auth()
    app.run(host='0.0.0.0')
