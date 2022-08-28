import time

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
from dash_extensions.enrich import Dash, Output, Input, State, Trigger, ServersideOutput

app = Dash(prevent_initial_callbacks=True)
app.layout = html.Div(
    [
        html.Button("Query data", id="btn"),
        dcc.Dropdown(id="dd"),
        dcc.Graph(id="graph"),
        dcc.Loading(dcc.Store(id="store"), fullscreen=True, type="dot"),
    ]
)


@app.callback(
    [ServersideOutput("store", "data"), ServersideOutput("store", "years")],
    Trigger("btn", "n_clicks"),
    State("store", "years"),
)
def query_data(years):
    time.sleep(1)
    df = px.data.gapminder()
    years_updated = list(df["year"])
    if years_updated == years:
        years_updated = dash.no_update
    return df, years_updated


@app.callback([Output("dd", "options"), Output("dd", "value")], Input("store", "years"))
def update_dd(years):
    if isinstance(years, type(dash.no_update)):
        raise dash.exceptions.PreventUpdate
    return [{"label": year, "value": year} for year in years], years[0]


@app.callback(Output("graph", "figure"), [Input("store", "data"), Input("dd", "value")])
def update_graph(df, value):
    df = df.query("year == {}".format(value))
    return px.sunburst(df, path=["continent", "country"], values="pop", color="lifeExp", hover_data=["iso_alpha"])


if __name__ == "__main__":
    app.run_server()
