import os
import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import pathlib


DATA_PATH = pathlib.Path().resolve()
df = pd.read_csv(DATA_PATH / "global_water.csv")

if not (DATA_PATH / "global_water.csv").exists():
    raise FileNotFoundError("global_water.csv not found in the project directory.")


country_list = sorted(df["Country"].unique())
year_list = sorted(df["Year"].unique())

sector_colors = {
    "Agricultural Water Use (%)": "#2ca02c",
    "Industrial Water Use (%)": "#FFA15A", 
    "Household Water Use (%)": "#636EFA"  
}

kpi_card_style = {
    "backgroundColor": "white",
    "minHeight": "90px",
    "overflow": "visible"
}

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.LUX])
app.title = "Global Water Dashboard"
server = app.server
app.config.suppress_callback_exceptions = True

app.layout = dbc.Container([
    dbc.Navbar(
        dbc.Container([
            html.Div([
                html.H3("Global Water Use and Sustainability", className="mb-0 text-white"),
                html.P("Compare rainfall, consumption, and scarcity across countries and years.",
                       className="mb-0 text-white-50", style={"fontSize": "0.9rem"})
            ])
        ]),
        color="primary",
        dark=True,
        className="mb-4"
    ),

    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H5("Filters", className="card-title mb-3"),
                    
                    dbc.Label("Country"),
                    dcc.Dropdown(
                        options=[{"label": c, "value": c} for c in country_list],
                        value=country_list[0],
                        id="country-select",
                        clearable=False
                    ),
                    dbc.Label("Year", className="mt-3"),
                    dcc.Dropdown(
                        options=[{"label": y, "value": y} for y in year_list],
                        value=year_list[-1],
                        id="year-select",
                        clearable=False
                    )
                ])
            ])
        ], width=2),

        dbc.Col([
            dbc.Row([
                dbc.Col(dbc.Card([
                    dbc.CardBody([
                        html.H6("Total Consumption (Billion m³)", className="card-title"),
                        html.H4(id="kpi-water", className="card-text")
                    ], style=kpi_card_style)
                ]), width=4),

                dbc.Col(dbc.Card([
                    dbc.CardBody([
                        html.H6("Annual Rainfall (mm)", className="card-title"),
                        html.H4(id="kpi-rain", className="card-text")
                    ], style=kpi_card_style)
                ]), width=4),

                dbc.Col(id="kpi-scarcity-box", width=4)
            ], className="mb-4", style={"overflow": "visible"}),

            dbc.Row([
                dbc.Col(dbc.Card([
                    dbc.CardBody([
                        html.H5("Per Capita Water Use Comparison", className="card-title"),
                        html.P("Compares selected year to the previous year", className="card-subtitle text-muted"),
                        dcc.Graph(id="compare-bar")
                    ], style={"paddingTop": "10px", "overflow": "visible"})
                ]), width=6),

                dbc.Col(dbc.Card([
                    dbc.CardBody([
                        html.H5("Water Use by Sector", className="card-title"),
                        html.P("Proportional water consumption across agriculture, industry, and households", className="card-subtitle text-muted"),
                        dcc.Graph(id="sector-pie")
                    ], style={"paddingTop": "10px", "overflow": "visible"})
                ]), width=6)
            ], className="mb-4"),

            dbc.Row([
                dbc.Col(dbc.Card([
                    dbc.CardBody([
                        html.H5("Rainfall vs Groundwater Depletion", className="card-title"),
                        html.P("Annual rainfall (left axis) agianst groundwater depletion rate (right axis)", className="card-subtitle text-muted"),
                        dcc.Graph(id="rain-deplete-scatter")
                    ], style={"paddingTop": "10px", "overflow": "visible"})
                ]), width=6),

                dbc.Col(dbc.Card([
                    dbc.CardBody([
                        html.H5("Historical Total Water Consumption", className="card-title"),
                        html.P("Long-term water consumption trends compared to overall average", className="card-subtitle text-muted"),
                        dcc.Graph(id="historical-line")
                    ], style={"paddingTop": "10px", "overflow": "visible"})
                ]), width=6)
            ], className="mb-4")
        ], width=10)
    ]),
    dbc.Row([
        dbc.Col(
            html.Footer("Data Source: Global Water Consumption Dataset (2000-2024)"),
            width=12,
            className="text-center text-muted my-4"
        )
    ])
], fluid=True)


@app.callback(
    [
        Output("sector-pie", "figure"),
        Output("rain-deplete-scatter", "figure"),
        Output("compare-bar", "figure"),
        Output("historical-line", "figure"),
        Output("kpi-water", "children"),
        Output("kpi-rain", "children"),
        Output("kpi-scarcity-box", "children")
    ],
    [
        Input("country-select", "value"),
        Input("year-select", "value")
    ]
)
def update_graphs(country, year):
    dff = df.copy()
    dff = dff[dff["Country"] == country]
    current = dff[dff["Year"] == year]
    previous = dff[dff["Year"] == (year - 1)]

    kpi_water = f"{current['Total Water Consumption (Billion Cubic Meters)'].iloc[0]:,.1f}" if not current.empty else "N/A"
    kpi_rain = f"{current['Rainfall Impact (Annual Precipitation in mm)'].iloc[0]:,.0f}" if not current.empty else "N/A"
    
    scarcity = current['Water Scarcity Level'].iloc[0] if not current.empty else "N/A"
    color_map = {"Low": "success", "Moderate": "warning", "High": "danger"}

    kpi_scarcity = dbc.Card([dbc.CardBody([
        html.H6("Water Scarcity Level", className="card-title"),
        html.H4(scarcity, className="card-text")
    ], style={"minHeight": "90px", "overflow": "visible"})], color=color_map.get(scarcity, "secondary"), inverse=True)

    
    pie_fig = px.pie(
        current.melt(value_vars=[
            "Agricultural Water Use (%)", "Industrial Water Use (%)", "Household Water Use (%)"
        ]),
        names="variable", values="value",
        template="plotly_white",
        color="variable",
        color_discrete_map=sector_colors
    )

    bar_y = [
        previous["Per Capita Water Use (Liters per Day)"].iloc[0],
        current["Per Capita Water Use (Liters per Day)"].iloc[0]
    ]

    bar_fig = px.bar(
        x=[f"{year-1}", f"{year}"],
        y=bar_y,
        labels={"x": "Year", "y": "Liters per Day"},
        template="plotly_white"
    )

    bar_fig.update_traces(
        marker_color=["#636EFA", "#EF553B"]
    )

    
    rainfall_trace = go.Scatter(
        x=dff["Year"],
        y=dff["Rainfall Impact (Annual Precipitation in mm)"],
        name="Rainfall (mm)",
        line=dict(color="#636EFA", width=3),
        yaxis="y1"
    )

    depletion_trace = go.Scatter(
        x=dff["Year"],
        y=dff["Groundwater Depletion Rate (%)"],
        name="Depletion Rate (%)",
        line=dict(color="#EF553B", width=3, dash="dash"),
        yaxis="y2"
    )

    scatter_fig = go.Figure(data=[rainfall_trace, depletion_trace])

    scatter_fig.update_layout(
        template="plotly_white",
        xaxis_title="Year",
        yaxis=dict(
            title=dict(text="Rainfall (mm)", font=dict(color="#636EFA")),
            tickfont=dict(color="#636EFA")
        ),
        yaxis2=dict(
            title=dict(text="Depletion Rate (%)", font=dict(color="#EF553B")),
            tickfont=dict(color="#EF553B"),
            anchor="x",
            overlaying="y",
            side="right",
            rangemode="tozero"
        ),
        legend=dict(
            orientation="h",
            yanchor="top",
            y=-0.25,
            xanchor="center",
            x=0.5
        ),
        margin=dict(l=60, r=60, t=40, b=60))

        
    avg_val = dff["Total Water Consumption (Billion Cubic Meters)"].mean()

    hist_fig = px.line(
        dff,
        x="Year",
        y="Total Water Consumption (Billion Cubic Meters)",
        labels={"Total Water Consumption (Billion Cubic Meters)": "Total Water Consumption (billion m³)"},
        template="plotly_white",
        markers=True,
        line_shape="linear"
    )

    hist_fig.update_traces(name="Total Water Consumption")
    hist_fig.add_scatter(
        x=dff["Year"],
        y=[avg_val] * len(dff),
        mode="lines",
        name="Overall Avg. Total Water Consumption",
        line=dict(dash="dash", color="#FFA15A")
    )

    hist_fig.update_layout(
        legend=dict(orientation="h", yanchor="top", y=-0.25, xanchor="center", x=0.5)
    )

    return pie_fig, scatter_fig, bar_fig, hist_fig, kpi_water, kpi_rain, kpi_scarcity

port = int(os.environ.get("PORT", 8050))

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=port)
