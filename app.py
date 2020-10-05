import dash 
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.express as px
import numpy as np



# Fetch Dataset into DataFrame
df = pd.read_csv('shutdown-data.csv')

#convert start_date to datetime object
df['start_date'] = pd.to_datetime(df['start_date'])

# define first plot and aesthetics
annual_shutdowns = px.bar(
    df, 
    x="start_date",
    range_x=['2019-05-01','2019-07-31'],
    color="affected_network",
    y="duration",
    log_y=True,
    title="Shutdowns by Duration",
    labels={'duration': 'Duration in days (log)', 'start_date': 'Date', 'affected_network': 'Affected Network'},
    hover_name="country ", hover_data=["duration"] 
)

annual_shutdowns.update_xaxes(
    rangeslider_visible = True,
    ticktext=["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"],
    tickvals=["2019-01-01","2019-02-01","2019-03-01","2019-04-01","2019-05-01","2019-06-01","2019-07-01","2019-08-01","2019-09-01","2019-10-01","2019-11-01","2019-12-01", ]
)
annual_shutdowns.update_yaxes(fixedrange = False)

# define second plot and aesthetics
downtime_country = px.pie(
    df,
    values="duration",
    names="country ",
    title="Shutdown Duration (of Total Global Downtime) by Country",    
)
downtime_country.update_traces(
    textposition='inside',
    textfont_size=14,
    textinfo="label+percent"
)

# sum instances of social media outtages
FB_count = df['Facebook_affected'].sum()
TW_count = df['Twitter_affected'].sum()
WA_count = df['WhatsApp_affected'].sum()
TG_count = df['Telegram_affected'].sum()

# create new dataframe
data = [('Facebook', FB_count), ('Twitter', TW_count), ('WhatsApp', WA_count), ('Telegram', TG_count)]
new_df = pd.DataFrame.from_records(data, columns=['service', 'outages'])

# define third plot and aesthetics
soc_shutdown = px.bar(
    new_df,
    x='service',
    y='outages',
    title="Social Media Shutdown by Platform",
    color="service"    
)

app = dash.Dash(__name__)

app.layout = html.Div([

    html.Div([
        html.Link(
            rel='stylesheet',
            href='/static/stylesheet.css'
        )
    ]),

    html.Div([
        html.H2('Global Internet Shutdowns in 2019'),

        html.P("Based on: Access Now's Shutdown Tracker Optimization Project (STOP)"),

        html.P('www.accessnow.org/keepiton')
    ]),

    html.Div([
    dcc.Graph(
        id='graph',
        figure=annual_shutdowns
    ),

    html.Hr([]),

    html.Div([
        dcc.Graph(
            id="pie",
            figure=downtime_country
        )
    ], className = "five columns"),
    
    html.Div([
        dcc.Graph(
            id="pie-2",
            figure=soc_shutdown         
        )
    ], className="five columns"),                   
], className="row")    

])

@app.server.route('/static/<path:path>')
def static_file(path):
    static_folder = os.path.join(os.getcwd(), 'static')
    return send_from_directory(static_folder, path)

if __name__ == '__main__':
    app.run_server(debug=True)



   
