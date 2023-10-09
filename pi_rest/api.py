from flask import Flask, Blueprint, request
from flask_cors import CORS
import subprocess
import hashlib
import hmac
import base64
import os

TOKEN = os.environ["WEBHOOK_REST_API_KEY"]
app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})

blueprint_name = Blueprint('blueprint_name', __name__)


def verify_webhook(secret, data, hmac_header):
    digest = hmac.new(secret.encode('utf-8'), data, digestmod=hashlib.sha256).digest()
    computed_hmac = base64.b64encode(digest)
    computed_hmac_hex = "sha256=" + base64.b64decode(computed_hmac.decode()).hex()

    return computed_hmac_hex == hmac_header


@blueprint_name.route('/pull_package', methods=['POST'])
def pull_package():
    print("Pull Package")

    package = request.args.get("package", None)
    is_good = verify_webhook(TOKEN, request.get_data(), request.headers.get('X-Hub-Signature-256'))

    if package and is_good:
        subprocess.run(f"cd ~/Documents/python/{package}; git pull", shell=True)

    return {}


app.register_blueprint(blueprint_name, url_prefix='/')

if __name__ == '__main__':
    ip = 'localhost'
    port = 8080

    app.run(host=ip, port=port, debug=False)
