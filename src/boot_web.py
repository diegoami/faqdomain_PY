
import yaml
from web import *
from application import Application

from werkzeug.contrib.fixers import ProxyFix
import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
app.wsgi_app = ProxyFix(app.wsgi_app)

config = yaml.safe_load(open("../config.yml"))
key_config = yaml.safe_load(open(config["key_file"]))
key_config.get("secret_key")
app.config['SECRET_KEY'] = key_config.get("secret_key")
app.application = Application(config)
if __name__ == '__main__':
    app.run(debug=True,  use_reloader=False , port=9091)