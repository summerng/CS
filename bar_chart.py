#import plotly.express as px
import plotly.graph_objects as go
import requests
from file_reader import file_reader
from file_reader import ask_for_csv_filename

def compose_bar_chart():

    # Print opening message for this program action
    print(
    """
    ================================================================================
    =                         Compose histogram chart                              =
    ================================================================================
    """
    )

    # Gets the lists of ids and quality of life scores
    ids, scores = file_reader(ask_for_csv_filename())

    # Get NY quality of life score
    base_url = "https://api.teleport.org/api/urban_areas/slug:new-york/scores/"
    r = requests.get(base_url)
    d = r.json()
    city_score = d["teleport_city_score"]

    # Get average sentiment score from csv file
    avg_sentiment = sum(scores) / len(scores)

    # fig = px.histogram(scores, x=scores, nbins=20, labels={'x' : "Quality of Life Metric"})
            
    # fig.show()

    fig = go.Figure()
    fig.add_trace(go.Histogram(
    x=scores,
    name='Quality of Life Name', # name used in legend and hover labels
    xbins=dict( # bins used for histogram
        start=0,
        end=100,
        size=5
    ),
    #marker_color='Red',
    opacity=1,
    marker=dict(
        line=dict(
            width = 2
        ),
        cmin=0,
        cmax=1,
        colorscale=[[0, 'rgb(0,0,255)'], [1, 'rgb(255,0,0)']]
        #color="Green"
    )
    ))

    fig.update_layout(
        title_text='Quality of Life Metrics for Headlines and Abstracts', # title of plot
        xaxis_title_text='Quality of Life Metric', # xaxis label
        yaxis_title_text='Frequency', # yaxis label
        # bargap=0.2, # gap between bars of adjacent location coordinates
    )

    fig.add_shape(
        go.layout.Shape(
            type="line",
            x0=avg_sentiment,
            y0=0,
            x1=avg_sentiment,
            y1=50,
            line=dict(
                color="red",
                width=3
            )
        )
    )

    fig.add_trace(go.Scatter(
        x=[avg_sentiment + 8],
        y=[15],
        text=["Average Sentiment Score: ({})".format(round(avg_sentiment, 2))],
        mode="text"
    ))

    fig.add_shape(
    go.layout.Shape(
        type="line",
        x0=city_score,
        y0=0,
        x1=city_score,
        y1=50,
        line=dict(
            color="yellow",
            width=3
        )
    )
    )

    fig.add_trace(go.Scatter(
        x=[city_score + 8],
        y=[15],
        text=["QOL Score for New York: ({})".format(round(city_score, 2))],
        mode="text"
    ))

    fig.show()
