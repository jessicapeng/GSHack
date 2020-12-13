"""
IPv6 Sec-Check Main Controller app.py
@author: Jessica Peng
"""

#imports and dependencies for main controller - lib
from flask import Flask, render_template, request, jsonify
from datetime import datetime
#from api import script

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
        form = request.form
        print(request.form)
        start_date=form["s-year"]+"-"+form["s-month"]+"-"+form["s-year"]
        end_date=form["e-year"]+"-"+form["e-month"]+"-"+form["e-year"]
        print("start_date", start_date, "end_date", end_date)
        #call script.runplots, etc; 
        return render_template("plot.html")
    

    
#start the server
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)

    
