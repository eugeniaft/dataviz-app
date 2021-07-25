import pandas as pd
import plotly.express as px


def data_loader(country='Brazil'):
    dt_url = 'https://covid.ourworldindata.org/data/owid-covid-data.csv'
    df = pd.read_csv(dt_url)
    df['date'] = pd.to_datetime(df.date)
    df['cfr'] = df['new_deaths_smoothed'] / df['new_cases_smoothed']
    df['v_1d_pct'] = df['people_vaccinated'] / df['population']
    df['v_1d_pct'] = df['v_1d_pct'].apply(lambda x: round(x*100, 2))
    df['v_2d_pct'] = df['people_fully_vaccinated'] / df['population']
    df['v_2d_pct'] = df['v_2d_pct'].apply(lambda x: round(x*100, 2))

    return df[df.location == country]


def line_plot(data, x, y, c, ylab, title):

    fig = px.line(data, x, y, title=title, template="ggplot2")
    fig.update_traces(line_color=c)

    fig.update_traces(hovertemplate='%{x}<br>%{y: .2f}')
    fig.update_layout(
        height=500,
        width=750,
        yaxis=dict(
            title=ylab,
            ),
        xaxis=dict(
            title='',
            ),
        )

    return fig


def two_line_plot(data, x, y1, y2, c1, c2,
                  ylab, label1, label2, title):

    fig = px.line(data, x, y=[y1, y2], title=title, template="ggplot2")
    fig['data'][0]['line']['color'] = c1
    fig['data'][1]['line']['color'] = c2
    fig['data'][0]['name'] = label1
    fig['data'][1]['name'] = label2

    fig.update_traces(hovertemplate='%{x}<br>%{y}%<extra></extra>')
    fig.update_layout(
        height=500,
        width=750,
        yaxis=dict(
            title=ylab,
            ),
        xaxis=dict(
            title='',
            ),
        legend=dict(title_text='')
        )

    return fig


def make_plots(df, type='vax'):

    if type == 'cases':
        plot = line_plot(df, 'date', 'new_cases_smoothed',
                         '#FF8370', 'Number of new cases',
                         'New Covid-19 cases')
    elif type == 'fatality':
        plot = line_plot(df, 'date', 'cfr',
                         '#E42256', 'Case fatality ratio',
                         'Case Fatality Ratio')
    elif type == 'vax':
        plot = two_line_plot(df, 'date', 'v_1d_pct', 'v_2d_pct',
                             '#00B1B0', '#FEC84D',
                             '% of the population vaccinated',
                             'At least 1 dose', 'Fully vaccinated',
                             'Vaccinations')
    return plot
