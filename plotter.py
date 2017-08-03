import matplotlib

from flask import Flask, make_response
from flask import jsonify
from flask import request
from urllib import urlencode 
import requests
import pandas 
import matplotlib.pyplot as plt
import seaborn as sbn

from StringIO import StringIO

from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.dates import DateFormatter

app = Flask(__name__)

def carto_query(query,username,api_key):
    
    params = {'q' : query, 'format':'csv'}
    if api_key:
        params['api_key'] = api_key

    url = 'https://{}.carto.com/api/v2/sql?'.format(username) + urlencode(params)
    return pandas.read_csv(url)


def mpl2img(fig):
    
    canvas = FigureCanvas(fig)
    img = StringIO()
    canvas.print_png(img)
    res = make_response(img.getvalue())
    res.headers['Content-Type'] = 'image/png'
    return res

@app.route('/pairplot.img')
def pairplot():
    
    query       = request.args.get('q')
    print(" QUERY IS ")
    print(query)
    username    = request.args.get('username')
    api_key     = request.args.get('apikey')

    xlabel      = request.args.get('xlabel')
    ylabel      = request.args.get('ylabel')
    title       = request.args.get('title')
    
    data = carto_query(query,username,api_key).fillna(0)

    plot = sbn.pairplot(data, kind='reg',markers='.')
    return mpl2img(plot.fig)


@app.route('/time.img')
def time():
    
    query       = request.args.get('q')
    username    = request.args.get('username')
    api_key     = request.args.get('apikey')

    xlabel      = request.args.get('xlabel')
    ylabel      = request.args.get('ylabel')
    title       = request.args.get('title')

    data = carto_query(query,username,api_key)
    print(data.set_index('cat'))

    fig = Figure()
    ax = fig.add_subplot(111)
    
    data.plot(kind='line',x='time',y='val',ax=ax)

    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    return mpl2img(fig)

@app.route('/bar.img')
def bar():
    
    query       = request.args.get('q')
    username    = request.args.get('username')
    api_key     = request.args.get('apikey')

    xlabel      = request.args.get('xlabel')
    ylabel      = request.args.get('ylabel')
    title       = request.args.get('title')

    data = carto_query(query,username,api_key)
    print(data.set_index('cat'))

    fig = Figure()
    ax = fig.add_subplot(111)
    data.set_index('cat').plot(kind='barh',ax=ax)
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    return mpl2img(fig)

@app.route('/scatter.img')
def scatter():
    query       = request.args.get('q')
    username    = request.args.get('username')
    api_key     = request.args.get('apikey')

    xlabel      = request.args.get('xlabel')
    ylabel      = request.args.get('ylabel')
    title       = request.args.get('title')


    
    data= carto_query(query, username,api_key)

    fig = Figure()
    ax = fig.add_subplot(111)
    data.plot(kind='scatter',x='x', y='y', ax=ax, marker='.')
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)


    return mpl2img(fig)
    
if __name__ == '__main__':
    print("HEY")
    app.run()
