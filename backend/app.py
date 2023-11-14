from flask import Flask, request, render_template, Blueprint
from routes.principal import principal_bp
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)
UPLOAD_FOLDER = 'storage'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


app.register_blueprint(principal_bp)

if __name__ == '__main__':
    app.run(debug=True, port=5000)