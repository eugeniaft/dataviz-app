from flask import Flask, render_template, request
import json
import plotly
from plots import covid_viz


app = Flask(__name__)


BASE_URL = "http://localhost:5000/"


@app.route('/callback', methods=['POST', 'GET'])
def cb():
    return covid_plots(request.args.get('data'))


@app.route('/', methods=['POST', 'GET'])
def index():
    graphJSON = covid_plots('Brazil')

    return render_template('index.html',
                           graphJSON=graphJSON,
                           ids=['grph1', 'grph2', 'grph3'])


def covid_plots(country='Brazil'):
    grph1 = cases(country)
    grph2 = fatality(country)
    grph3 = vaccines(country)
    plots = [grph1, grph2, grph3]
    graphJSON = json.dumps(plots, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON


def cases(country='Brazil'):
    df = covid_viz.data_loader(country)
    fig = covid_viz.make_plots(df, type='cases')
    return fig


def fatality(country='Brazil'):
    df = covid_viz.data_loader(country)
    fig = covid_viz.make_plots(df, type='fatality')
    return fig


def vaccines(country='Brazil'):
    df = covid_viz.data_loader(country)
    fig = covid_viz.make_plots(df, type='vax')
    return fig


if __name__ == '__main__':
    app.run(debug=False)
