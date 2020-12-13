"""
IPv6 Sec-Check Main Controller app.py
@author: Jessica Peng
"""

#imports and dependencies for main controller - lib

from flask import Flask, render_template, request, jsonify, redirect, url_for, Response
import datetime

import pandas_datareader as pdr
import matplotlib.pyplot as plt
from scipy import stats
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

    plt.close()

    fig = create_covid_figure(start, end)
    plt.savefig('frontend/static/img/cases.png')

    plt.close()

    corr = calculate_correlation(start, end)

    return render_template("plot.html", start=start, end=end, corr=corr)

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

    start_split = str(start_date).split("-")
    end_split = str(end_date).split("-")

    start = datetime.datetime(int(start_split[0]), int(start_split[1]), int(start_split[2]))
    end = datetime.datetime(int(end_split[0]), int(end_split[1]), int(end_split[2]))

    df3 = pd.read_csv("covid_data_who.csv")

    df3['date'] = pd.to_datetime(df3['date'])

    mask = (df3['date'] >= start) & (df3['date'] <= end)
    df4 = df3.loc[mask]

    graph = df4.plot(x='date', y='totalConfirmed', grid=True, figsize=(12, 8), title="Total Confirmed Cases by WHO", lw=4)
    graph.set_ylabel("Daily Total Confirmed Cases")
    graph.set_facecolor("#000000")

    return graph.get_figure()

def calculate_correlation(start_date, end_date):

    start_split = str(start_date).split("-")
    end_split = str(end_date).split("-")

    start = datetime.datetime(int(start_split[0]), int(start_split[1]), int(start_split[2]))
    end = datetime.datetime(int(end_split[0]), int(end_split[1]), int(end_split[2]))

    sp500 = pdr.get_data_yahoo('VOO', start=start, end=end)
    sp_pct_change = np.mean(np.array(sp500['Adj Close'].pct_change()[1:]))
    
    df = pd.read_csv("covid_data_who.csv")
    df['date'] = pd.to_datetime(df['date'])

    mask = (df['date'] >= start) & (df['date'] <= end)
    df2 = df.loc[mask]

    sp2 = sp500['Adj Close']
    sp2.index = pd.DatetimeIndex(sp2.index)
    sp2 = sp2.reindex(pd.date_range(start, end), fill_value=0)

    for i in range(1, len(sp2)):
        if sp2[i] == 0:
            sp2[i] = sp2[i-1] * (1 + sp_pct_change)

    corr = stats.pearsonr(sp2, df2['totalConfirmed'])

    return corr[0]

    
#start the server
if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000, debug=True)

    
