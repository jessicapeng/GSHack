"""
IPv6 Sec-Check Main Controller app.py
@author: Jessica Peng
"""

#imports and dependencies for main controller - lib
<<<<<<< HEAD
from flask import Flask, render_template, request, jsonify
from datetime import datetime
#from api import script
=======
from flask import Flask, render_template, request, jsonify, redirect, url_for, Response
import datetime
# from gs_quant.session import GsSession, Environment

import pandas_datareader as pdr
import matplotlib.pyplot as plt
matplotlib.use('Agg')
import pandas as pd
import numpy as np
>>>>>>> db1917b5de871aefd8b91bbe495c2b6550b98b02

import json
import requests
import io

from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas


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
        return redirect(url_for("plot_png"))
        # return render_template("plot.html")

@app.route('/plot.html')
def plot():

    # if request.method == "POST":
    #     return redirect(url_for("index"))

    # fig = create_figure()
    # plt.savefig('frontend/templates/plot.png')
    return render_template("plot.html")

@app.route('/plot.png')
def plot_png():

    fig = create_figure()
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')


def create_figure():

    # GsSession.use(client_id='c8a9707af9bc453e8f08f69eb44d1d0a',
    #     client_secret='e36e001a7ab7205c46d7e9d09794b46f1b019f0d71d5857c4bdf7681f2c24e6a',
    #     scopes=('read_product_data',))

    start = datetime.date(2020, 6, 21)
    end = datetime.date(2020, 12, 1)

    sp500 = pdr.get_data_yahoo('VOO', start=start, end=end)

    smallcap = pdr.get_data_yahoo('VB', start=start, end=end)
    midcap = pdr.get_data_yahoo('VO', start=start, end=end)
    largecap = pdr.get_data_yahoo('VV', start=start, end=end)

    df = pd.DataFrame()
    df['S&P500'] = sp500['Adj Close']
    df['Small Cap'] = smallcap['Adj Close']
    df['Mid Cap'] = midcap['Adj Close']
    df['Large Cap'] = largecap['Adj Close']

    graph = df.plot(y=['S&P500', 'Small Cap', 'Mid Cap', 'Large Cap'], figsize=(12, 8), lw=4, title="Adjusted Close Prices", grid=True)
    graph.set_ylabel("Daily Adjusted Close Price")
    graph.set_facecolor("#000000")

    return graph.get_figure()

    # who_dataset = Dataset('COVID19_COUNTRY_DAILY_WHO')
    # data_frame = who_dataset.get_data(countryId='US', start=start, end=end)
>>>>>>> db1917b5de871aefd8b91bbe495c2b6550b98b02

    # ax = data_frame['totalConfirmed'].plot(grid=True, figsize=(12, 8), title="Total Confirmed Cases by WHO", lw=4)
    # ax.set_ylabel("Daily Total Confirmed Cases")
    # ax.set_facecolor("#000000")  
    
#start the server
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)

    
