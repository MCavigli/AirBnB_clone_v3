#!/usr/bin/python3
from flask import Flask, render_template
from models import storage
from api.v1.views import app_views
from os import getenv
app = Flask(__name__)
app.register_blueprint(app_views)
app.url_map.strict_slashes = False
ip = getenv("HBNB_API_HOST") or '0.0.0.0'
port = getenv("HBNB_API_PORT") or 5000


@app.teardown_appcontext
def teardown(self):
    # tears down app context
    storage.close()

if __name__ == '__main__':
    app.run(host=ip, port=port, threaded=True)
