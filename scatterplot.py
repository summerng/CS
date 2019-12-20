import os
import plotly.express as px
import plotly.graph_objects as go
import requests
from file_reader import file_reader
from file_reader import file_reader
from file_reader import ask_for_csv_filename


def scatterplot():

    print(
    """
    ================================================================================
                               = Creating scatterplot =
    ================================================================================
    """
    )

    base_url = "https://api.teleport.org/api/urban_areas/slug:new-york/scores/"
    r = requests.get(base_url)
    d = r.json()
    city_score = d["teleport_city_score"]
    avg_sentiment = 0

    t = file_reader(ask_for_csv_filename())
    for sentiment in t[1]:
        avg_sentiment += sentiment
    avg_sentiment = avg_sentiment / len(t[1])

    fig_scatter = px.scatter(x=t[0], y= t[1],
                color=t[1], color_continuous_scale='Magma')
    fig_scatter.add_shape(
        # Line Horizontal
        go.layout.Shape(
            type="line",
            x0=-5,
            y0=avg_sentiment,
            x1=105,
            y1=avg_sentiment,
            line=dict(
                color="black",
                width=3
            )
    ))
    fig_scatter.add_shape(
        # Line Horizontal
        go.layout.Shape(
            type="line",
            x0=-5,
            y0=city_score,
            x1=105,
            y1=city_score,
            line=dict(
                color="black",
                width=3
            )
    ))
    # Create scatter trace of text labels
    fig_scatter.add_trace(go.Scatter(
        x=[5, 5],
        y=[avg_sentiment + 2, city_score + 2],
        text=["Average Sentiment Score",
          "Quality of Life Score for New York"],
        mode="text",
))
    
    fig_scatter.update_layout(
        title="Sentiment Score for Each Headline/Abstract",
        xaxis_title="Headline/Abstract ID",
        yaxis_title="Sentiment Score (out of 100)"
    )

    fig_scatter.show()