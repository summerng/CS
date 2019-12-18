#import plotly.express as px
import plotly.graph_objects as go
from file_reader import file_reader
from file_reader import ask_for_csv_filename

def compose_bar_chart():

    # Print opening message for this program action
    print(
    """
    ================================================================================
    =                              Compose bar chart                               =
    ================================================================================
    """
    )

    # Gets the lists of ids and quality of life scores
    ids, scores = file_reader(ask_for_csv_filename())

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
            x0=29,
            y0=0,
            x1=29,
            y1=20,
            line=dict(
                color="red",
                width=3
            )
        )
    )

    fig.add_trace(go.Scatter(
        x=[36.5],
        y=[15],
        text=["Average Sentiment Score: (~29)"],
        mode="text"
    ))

    fig.add_shape(
    go.layout.Shape(
        type="line",
        x0=69,
        y0=0,
        x1=69,
        y1=20,
        line=dict(
            color="yellow",
            width=3
        )
    )
    )

    fig.add_trace(go.Scatter(
        x=[76],
        y=[15],
        text=["QOL Score for New York: (~69)"],
        mode="text"
    ))

    fig.show()
