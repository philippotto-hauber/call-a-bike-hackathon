#%% libs
import pandas as pd
import plotly.express as px

#%% load data

dat_plot = pd.read_csv("./plots/data/trips_heatmap/dat_trips_heatmap.csv")

#%% plot
fig = px.imshow(dat_plot,
                labels = dict(x = "start", y = "end", color = "trips"),
                color_continuous_scale='Blues',
                aspect="auto",
                title = "Number of trips by start and end station")
fig.update_xaxes(showticklabels=False)
fig.update_yaxes(showticklabels=False)
fig.show()