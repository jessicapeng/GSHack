"""
IPv6 Sec-Check Main Controller app.py
@author: Jessica Peng
"""

#imports and dependencies for main controller - lib
from flask import Flask, render_template, request, jsonify
from datetime import datetime
from api import script

import json
import requests 

#paths
TEMPLATES_PATH = 'frontend/templates/'
STATIC_PATH = 'frontend/static/'
API_PATH = 'api'

#Flask app variable
app = Flask(__name__, static_folder=STATIC_PATH, template_folder=TEMPLATES_PATH)


#loads pages of web app from GET or POST requests
@app.route('/', methods=['GET', 'POST'])
def index():

    #GET request to load security page
    if request.method == "GET":
        return render_template("index.html")
    if request.method == "POST":
        print(request.form)
        
        return render_template("plot.html")

    
#start the server
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)

    
