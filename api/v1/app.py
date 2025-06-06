#!/usr/bin/python
from flask import Flask
from models import storage
from flask import jsonify
from api.v1.views import app_views
app = Flask(__name__)
app.register_blueprint(app_views, url_prefix='/api/v1')

@app.teardown_appcontext
def teardown_storage(exception):
    """Closes the storage session after each request"""
    storage.close()

@app.errorhandler(404)
def not_found(error):
    """Handles 404 errors"""
    return jsonify({"error": "Not found"}), 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)


