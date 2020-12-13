"""
IPv6 Sec-Check Main Controller app.py
@author: Jessica Peng
"""

#imports and dependencies for main controller - lib

from flask import Flask, render_template, request, jsonify, redirect, url_for, Response
import datetime

import pandas_datareader as pdr
import matplotlib.pyplot as plt
# matplotlib.use('Agg')
import pandas as pd
import numpy as np

import json
import requests
import io

# from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas


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
        start_date=form["s-year"]+"-"+form["s-month"]+"-"+form["s-day"]
        end_date=form["e-year"]+"-"+form["e-month"]+"-"+form["e-day"]
        print("start_date", start_date, "end_date", end_date)
        #call script.runplots, etc; 
        return redirect(url_for("plot", start=start_date, end=end_date))
        # return render_template("plot.html")

@app.route('/plot', methods=['GET', 'POST'])
def plot():

    # if request.method == "POST":
    #     return redirect(url_for("index"))

    start = request.args.get("start")
    end = request.args.get("end")

    fig = create_stock_figure(start, end)
    plt.savefig('frontend/static/img/plot.png')

    # fig = create_covid_figure(start, end)
    # plt.savefig('frontend/templates/cases.png')

    plt.close()

    return render_template("plot.html", start=start, end=end)

# @app.route('/plot.png')
# def plot_png():

#     fig = create_figure()
#     output = io.BytesIO()
#     FigureCanvas(fig).print_png(output)
#     return Response(output.getvalue(), mimetype='image/png')


def create_stock_figure(start_date, end_date):

    start_split = str(start_date).split("-")
    end_split = str(end_date).split("-")

    start = datetime.date(int(start_split[0]), int(start_split[1]), int(start_split[2]))
    end = datetime.date(int(end_split[0]), int(end_split[1]), int(end_split[2]))

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


def create_covid_figure(start_date, end_date):

    from gs_quant.session import GsSession, Environment
    from gs_quant.data import Dataset

    GsSession.use(client_id='c8a9707af9bc453e8f08f69eb44d1d0a',
        client_secret='e36e001a7ab7205c46d7e9d09794b46f1b019f0d71d5857c4bdf7681f2c24e6a',
        scopes=('read_product_data',))

    start_split = str(start_date).split("-")
    end_split = str(end_date).split("-")

    start = datetime.date(int(start_split[0]), int(start_split[1]), int(start_split[2]))
    end = datetime.date(int(end_split[0]), int(end_split[1]), int(end_split[2]))

    who_dataset = Dataset('COVID19_COUNTRY_DAILY_WHO')
    data_frame = who_dataset.get_data(countryId='US', start=start, end=end)

    ax = data_frame['totalConfirmed'].plot(grid=True, figsize=(12, 8), title="Total Confirmed Cases by WHO", lw=4)
    ax.set_ylabel("Daily Total Confirmed Cases")
    ax.set_facecolor("#000000")
    
#start the server
if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000, debug=True)

    
