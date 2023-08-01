# Import required libraries
import pandas as pd
import dash
from dash import html, dcc , Input, Output , callback
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center',
                                               'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(id='site-dropdown',
                                             options = [
                                                            {"label" : "All Sites" , "value" : "ALL"} ,
                                                            {"label" : "CCAFS LC-40" , "value" : "CCAFS LC-40"} ,
                                                            {"label" : "VAFB SLC-4E" , "value" : "VAFB SLC-4E"},
                                                            {"label" : "KSC LC-39A" , "value" : "KSC LC-39A"} ,
                                                            {"label" : "CCAFS SLC-40" , "value" : "CCAFS SLC-40"}
                                             ],
                                             value = "ALL" ,
                                             placeholder = "Select Launch Site" ,
                                             searchable = True,
                                             style = {"width" : "80%" , "margin" : "auto"}
                                ),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart' , style = {"width" :  "90%" , "margin" : "auto"}),
                                         style = {
                                                    "border" : "3px solid green",
                                                    "border-radius" : "20px",
                                                    "width" : "85%" ,
                                                    "margin" : "auto"
                                         }
                                ),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id="payload_slider" ,
                                                min = 0 ,
                                                max = 10000,
                                                step = 500,
                                                marks = {
                                                         0: "0" ,
                                                         2500 : "2500",
                                                         5000 : "5000" ,
                                                         7500 : "7500" ,
                                                         10000 : "10000"
                                                        },
                                                value = [min_payload, max_payload]
                                ),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart' , style = {"width" : "90%" , "margin" : "auto"}),
                                         style = {
                                                    "width" : "85%",
                                                    "margin" : "auto",
                                                    "border" : "3px solid green",
                                                    "border-radius" : "20px"
                                         }
                                ),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@callback(
            Output(component_id = "success-pie-chart" , component_property = "figure") ,
            Input(component_id = "site-dropdown" , component_property = "value")
)
def PieChart(Site):
    data = spacex_df[["Launch Site" , "class"]]
    if Site == "ALL" :
        succ = data[data["class"] == 1]
        rate = succ.groupby("Launch Site")["class"].sum().reset_index()
        fig = px.pie(rate , values = "class" , names = "Launch Site" , title = "Success rate for Every launch Site")
        return fig
    else :
        rate = data[data["Launch Site"] == Site].reset_index()
        List = [rate[rate["class"] == 1]["class"].count() , rate[rate["class"] == 0]["class"].count()]
        fig = px.pie(rate , values = List , names = ["1" , "0"] , title = f"Success Rate of {Site}")
        return fig
# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@callback(
            Output(component_id = "success-payload-scatter-chart" , component_property= "figure"),
            [Input(component_id = "payload_slider" , component_property = "value"),
             Input(component_id = "site-dropdown" , component_property = "value")]
)
def ScatterChart(Payload , Site):
    if Site == "ALL":
        data = spacex_df
        data = data[data["Payload Mass (kg)"] <= Payload[1]]
        data = data[data["Payload Mass (kg)"] >= Payload[0]]
        fig = px.scatter(data , x = "Payload Mass (kg)" , y = "class" , color = "Booster Version Category" , title = "Success rate scatter graph for all Sites")
        fig.update_layout(xaxis_title = f"Payload mass from {Payload[0]} to {Payload[1]} kg" , yaxis_title = "Success (0/1)")

        return fig
    else:
        data = spacex_df[spacex_df["Launch Site"] == Site]
        data = data.sort_values(by = ["Payload Mass (kg)"])
        data = data[data["Payload Mass (kg)"] <= Payload[1]]
        data = data[data["Payload Mass (kg)"] >= Payload[0]]
        fig = px.scatter(data , x = "Payload Mass (kg)" , y = "class" , color = "Booster Version Category" , title = f"Success rate scatter graph for {Site}")
        fig.update_layout(xaxis_title = f"Payload mass from {Payload[0]} to {Payload[1]} kg", yaxis_title = "Success (0/1)")
        return fig


# Run the app
if __name__ == '__main__':
    app.run_server(debug = True)
