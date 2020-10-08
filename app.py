# Import required libraries
import copy
import dash
import pandas as pd
import numpy as np
from dash.dependencies import Input, Output, State, ClientsideFunction
import dash_core_components as dcc
import dash_html_components as html
from covid_controls import Age_Group,Occupation
import plotly.express as px
import geopandas as gpd

def_week_range = [0,53]

app = dash.Dash(
     __name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}]
 )

app.title = 'morLAB COVID-19 Dashboard'
#app = JupyterDash(
#    __name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}]
#)
server = app.server

#df = pd.read_csv('./data/Canadian_Covid_Cases.csv',index_col=0, low_memory=False)

df = pd.read_csv("https://github.com/faraz2023/morlab-covid-dashboard/raw/master/data/Canadian_Covid_Cases.csv",index_col=0, low_memory=False)

#with open("canada1.geojson") as f:
#    geojson = json.load(f,strict=False)
geojson = gpd.read_file('https://github.com/faraz2023/morlab-covid-dashboard/raw/master/canada1.geojson')
geojson['geometry'] = geojson['geometry'].simplify(0.5, preserve_topology=False)

layout = dict(
    autosize=True,
    automargin=True,
    margin=dict(l=30, r=30, b=20, t=40),
    hovermode="closest",
    plot_bgcolor="#F9F9F9",
    paper_bgcolor="#F9F9F9",
    legend=dict(font=dict(size=10), orientation="h"),
    title="Satellite Overview",

)

age_group = [
    {"label": str(Age_Group[ag]), "value": str(ag)}
    for ag in Age_Group
]

gender_options={
"Male":1,
"Female":2,
"NS":9
}
occupation=[
    {"label": str(Occupation[occ]), "value": str(occ)}
    for occ in Occupation
]

controls_html = [

    html.P(
        "Filter by Episode Week",
        className="control_label",
    ),
    dcc.RangeSlider(
        id="week_slider",
        min=0,
        max=52,
        value=def_week_range,
        className="dcc_control",
    ),
     html.P(
        "Filter by gender",
        className="control_label",
    ),

    dcc.RadioItems(
        id="gender_selector",
        options=[
            {"label": "All", "value": "all"},
            {"label": "Female ", "value": "Female"},
            {"label": "Not Stated", "value": "NS"},
            {"label": "Male ", "value": "Male"},
        ],
        value="all",
        labelStyle={"display": "inline-block"},
        inputStyle={"margin":"5px"},
        className="dcc_control",
    ),
    html.P(
        "Filter by age group",
        className="control_label",
    ),

    dcc.Dropdown(
        id="age_group",
        options=age_group,
        multi=True,
        value=list(Age_Group.keys()),
        className="dcc_control",
        placeholder="Select an age group",

    ),
     
    html.P(
        "Filter by occupation",
        className="control_label",
    ),

    dcc.Dropdown(
        id="occupation",
        options=occupation,
        multi=True,
        value=list(Occupation.keys()),
        className="dcc_control",
        placeholder="Select an occupation",

    ),
]


counts_total_number=[
                                html.Div(
                                    [html.H6(id="death_text"), html.P("Deaths")],
                                    id="death",
                                    className="mini_container one-third column",
                                ),
                                html.Div(
                                    [html.H6(id="recovery_text"), html.P("Recovered")],
                                    id="recovery",
                                    className="mini_container one-third column",
                                ),
                                 html.Div(
                                    [html.H6(id="total_text"), html.P("Total Cases")],
                                    id="total",
                                    className="mini_container one-third column",
                                ),
                            ]

header_row = html.Div(
            [
                html.Div(
                    [
                        html.Img(
                            src=app.get_asset_url("logo.png"),
                            id="plotly-image",
                            style={
                                "height": "100px",
                                "width": "auto",
                                "margin-bottom": "20px",
                            },
                        )
                    ],
                    className="one-third column",
                ),
                html.Div(
                    [
                        html.Div(
                            [
                                html.H3(
                                    "Canadian COVID-19 Cases",
                                    style={"margin-bottom": "0px"},
                                ),
                                html.H5(
                                    "Prototype Presentation", style={"margin-top": "0px"}
                                ),
                            ]
                        )
                    ],
                    className="one-half column",
                    id="title",
                ),
                html.Div(
                    [
                        html.A(
                            html.Button("Learn More", id="learn-more-button"),
                            href="https://morlab.mie.utoronto.ca/",
                            target="_blank"
                        )
                    ],
                    className="one-third column",
                    id="button",
                ),
            ],
            id="header",
            className="row flex-display",
            style={"margin-bottom": "25px"},
    )

# Create app layout
app.layout = html.Div(
    [
        header_row,
        html.Div(
            [
                html.Div(
                    controls_html,
                    className="pretty_container four columns",
                    id="cross-filter-options",
                ),
                html.Div(
                    [
                        html.Div(
                            counts_total_number,
                            id="info-container",
                            className="row container-display",
                        ),
                        html.Div(
                            [dcc.Graph(id="weekly_count_graph")],
                            id="countGraphContainer",
                            className="pretty_container",
                        ),
                    ],
                    id="right-column",
                    className="eight columns",
                ),
            ],
            className="row flex-display",
        ),
        html.Div(
            [
                html.Div(
                    [dcc.Graph(id="main_graph")],
                    className="pretty_container seven columns",
                ),
                
                
                html.Div([
                    
                    dcc.RadioItems(
                    id="line_type",
                        options=[
                    {"label": "Total Cases", "value": "total"},
                    {"label": "Recovered", "value": "recovered"},
                    {"label": "Deaths", "value": "death"},
      
                    ],
                    value="total",
                    labelStyle={"display": "inline-block", "padding-right": "4px", "margin-top":"0px"},
                    inputStyle={"margin-right":"5px"},
                    className="dcc_control",
                    ),
                dcc.Graph(id="individual_graph"),
       
                ], className="pretty_container five columns",
                    style={"padding":"0", "margin-bottom":"-20px", "padding-left":"20px"},


                    
                ),
            ],
            className="row flex-display",
        ),

    ],
    id="mainContainer",
    style={"display": "flex", "flex-direction": "column"},
)


def filter_dataframe(df, age_group, gender_selector, occupation, week_range=def_week_range):

    if gender_selector == "all":
        filtered_df = df[
            df['Age group'].isin(age_group)
            & df['Occupation'].isin(occupation)
            & (df['Episode week'] >= week_range[0])
            & (df['Episode week'] <= week_range[1])
        ]

    else:
        filtered_df = df[
            df['Age group'].isin(age_group)
            & (df['Gender'] == gender_options.get(gender_selector))
            & df['Occupation'].isin(occupation)
            & (df['Episode week'] >= week_range[0])
            & (df['Episode week'] <= week_range[1])
        ]

    return filtered_df

# Slider -> count graph
@app.callback(Output("week_slider", "value"), [Input("weekly_count_graph", "selectedData")])
def update_year_slider(count_graph_selected):

    if count_graph_selected is None:
        return def_week_range

    nums = [int(point["pointNumber"]) for point in count_graph_selected["points"]]
    return [min(nums), max(nums) + 1]


@app.callback(
    [Output("death_text", "children"),
     Output("recovery_text", "children"),
     Output("total_text", "children"),
     ],

    [
        Input("age_group", "value"),
        Input("gender_selector", "value"),
        Input("occupation", "value"),
        Input("week_slider", "value")
    ],
)
def update_numbers(age_group, gender_selector, occupation, week_range):
    # To do: clean up to use the filter_dataframe function
    if gender_selector == "all":
        total = df[
            (df['Age group'].isin(age_group))
            & (df['Occupation'].isin(occupation))
            & (df['Episode week'] >= week_range[0])
            & (df['Episode week'] <= week_range[1])
        ].shape[0]

        num_of_death = df[
            (df['Death'] == 1)
            & (df['Age group'].isin(age_group))
            & (df['Occupation'].isin(occupation))
            & (df['Episode week'] >= week_range[0])
            & (df['Episode week'] <= week_range[1])
        ].shape[0]

        num_recovered = df[
            (df['Recovered'] == 1)
            & (df['Age group'].isin(age_group))
            & (df['Occupation'].isin(occupation))
            & (df['Episode week'] >= week_range[0])
            & (df['Episode week'] <= week_range[1])
        ].shape[0]

    else:
        num_of_death = df[
            (df['Death'] == 1)
            & (df['Gender'] == gender_options.get(gender_selector))
            & (df['Age group'].isin(age_group))
            & (df['Occupation'].isin(occupation))
            & (df['Episode week'] >= week_range[0])
            & (df['Episode week'] <= week_range[1])
        ].shape[0]

        num_recovered = df[
            (df['Recovered'] == 1)
            & (df['Gender'] == gender_options.get(gender_selector))
            & (df['Age group'].isin(age_group))
            & (df['Occupation'].isin(occupation))
            & (df['Episode week'] >= week_range[0])
            & (df['Episode week'] <= week_range[1])
        ].shape[0]

        total = df[
            df['Age group'].isin(age_group)
            & (df['Gender'] == gender_options.get(gender_selector))
            & (df['Occupation'].isin(occupation))
            & (df['Episode week'] >= week_range[0])
            & (df['Episode week'] <= week_range[1])
        ].shape[0]

    return [num_of_death, num_recovered, total]


# Selectors -> main graph
@app.callback(
    Output("main_graph", "figure"),
    [
        Input("age_group", "value"),
        Input("gender_selector", "value"),
        Input("occupation", "value"),
        Input("week_slider", "value")
    ],
)
def make_main_figure(age_group, gender_selector, occupation, week_range):
    filtered_df = filter_dataframe(df, age_group, gender_selector, occupation, week_range)
    death_number = filtered_df[filtered_df["Death"] == 1].groupby('Region').size()
    
    
    for i in range(1,6):
        if i not in death_number.index:
            death_number[i]=0



     

    data = {'Code': ["CA01", "CA11", "CA03", "CA05", "CA09", "CA07", "CA06", "CA13", "CA08", "CA04", "CA12", "CA02",
                     "CA10"],
            'Region': ["4", "4", "4", "1", "1", "1", "4", "3", "3", "1", "5", "5", "2"],

            'Region Name':["Prairies Provinces and the Northwest Territories","Prairies Provinces and the Northwest Territories","Prairies Provinces and the Northwest Territories","Atlantic Provinces","Atlantic Provinces","Atlantic Provinces","Prairies Provinces and the Northwest Territories","Ontario and Nunavut","Ontario and Nunavut","Atlantic Provinces","British Columbia and Yukon","British Columbia and Yukon","Quebec"],
            
            'Death': [death_number[4], death_number[4], death_number[4], death_number[1], death_number[1],
                      death_number[1], death_number[4], death_number[3], death_number[3], death_number[1],
                      death_number[5], death_number[5], death_number[2]]

            }

    fig = px.choropleth_mapbox(data, geojson=geojson, locations='Code', color='Region Name', featureidkey="properties.CODE",
                               custom_data=["Region"], hover_data=['Death'],
                               color_continuous_scale="Viridis",
                               range_color=(0, 12),
                               mapbox_style="carto-positron",
                               zoom=2, center={"lat": 65.1304, "lon": -106.3468},
                               opacity=0.5,
                               labels={'Region Name':'Region'}
                               )
    
    
    fig.update_layout(legend=dict(
    orientation="h",
    yanchor="bottom",
    y=1.02,
    xanchor="right",
    x=0.5
    ),margin={"r": 0,  "l": 0, "b":0})
    
    return fig


# # Main graph -> individual graph
@app.callback(Output("individual_graph", "figure"),
              [Input("main_graph", "hoverData"),
                    Input("line_type", "value")],
                [ State("age_group", "value"),
                    State("gender_selector", "value"),
                    State("occupation", "value"),
                    State("week_slider", "value")
                                                     ])
def make_individual_figure(main_graph_hover,line_type,age_group,gender_selector,occupation, week_range):
    layout_individual = copy.deepcopy(layout)

    if main_graph_hover is None:
        main_graph_hover = {
            "points": [
                {"curveNumber": 4, "pointNumber": 569, "customdata": 0}
            ]
        }
 
    
    chosen = np.asarray([point["customdata"] for point in main_graph_hover["points"]]).flatten()
    filtered_df = filter_dataframe(df, age_group, gender_selector, occupation, week_range)
    weekly_data = filtered_df[(filtered_df["Episode week"] != 99)& (filtered_df['Region'] == int(chosen[0]))]

    
    rc_weekly_data=weekly_data[weekly_data['Recovered']==1]
    recovered_data = rc_weekly_data.groupby(["Episode week"]).size().to_frame('Recovered').reset_index()
    d_weekly_data=weekly_data[weekly_data['Death']==1]
    death_data = d_weekly_data.groupby(["Episode week"]).size().to_frame('Death').reset_index()
    x_axis=df['Episode week']
    

    if line_type=="total":

        data = weekly_data.groupby(["Episode week"]).size().to_frame('Total Cases').reset_index()

        fig = px.line(data, x='Episode week', y='Total Cases')
       # fig.update_yaxes(range=[0, 900])

        
    elif line_type=="recovered":
        
        fig = px.line(recovered_data, x='Episode week', y='Recovered')
      #  fig.update_yaxes(range=[0, 900])

    elif line_type=="death":
 
        fig = px.line(death_data, x='Episode week', y='Death')
    #    fig.update_yaxes(range=[0, 200])
        
    fig.update_traces(mode='lines+markers')
    fig.update_layout(autosize=True,margin={"r": 0, "t":5, "l":50, "b":10})
         

    return fig


@app.callback(
    Output("weekly_count_graph", "figure"),
    [
        Input("age_group", "value"),
        Input("gender_selector", "value"),
        Input("occupation", "value"),
        Input("week_slider", "value")
    ],
)
def make_count_figure(age_group, gender_selector, occupation, week_range):


    layout_count = copy.deepcopy(layout)

    dff = filter_dataframe(df, age_group, gender_selector, occupation, def_week_range)

    count_df = dff['Episode week'].value_counts() \
        .to_frame('Count').rename_axis('Episode week') \
        .reset_index()

    g = count_df[["Count", "Episode week"]]
    g.index = g["Episode week"]
    g = g.sort_index()
   # g = g.resample("A").count()
    colors = ['' for i in range(def_week_range[0], def_week_range[1])]
    for i in range(def_week_range[0], def_week_range[1]):
        if (i >= int(week_range[0]) and i < int(week_range[1])):
            colors[i] = "rgb(123, 199, 255)"
           # colors.append("rgb(223, 199, 255)")
        else:
            colors[i] = "rgba(123, 199, 255, 0.2)"
           # colors.append("rgba(123, 199, 255, 0.2)")


    data = [
        dict(
            type="scatter",
            mode="markers",
            x=g.index,
            y=g["Count"],
            name="Case Count",
            opacity=0,
            hoverinfo="skip",
        ),
        dict(
            type="bar",
            x=g.index,
            y=g["Count"],
            name="Case Count",
            marker=dict(color=colors),
        ),
    ]

    layout_count["title"] = "Weekly Case Counts"
    layout_count["dragmode"] = "select"
    layout_count["showlegend"] = False
    layout_count["autosize"] = True

    figure = dict(data=data, layout=layout_count)
    return figure

if __name__ == '__main__':
    app.run_server(debug=True)
