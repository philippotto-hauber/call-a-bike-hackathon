#%% libs
import pandas as pd
import numpy as np
#import matplotlib
#import matplotlib as mpl
import matplotlib.pyplot as plt
import plotly.express as px

#%% load data

dat_raw = pd.read_csv('./data/biketrip_data.csv')
dat_stations = dat_raw[['start_station_id', 'end_station_id', 'datetime_from']]

# %% load rental zone data to get full name of stations
dat_rental_zone = pd.read_csv('./data/OPENDATA_RENTAL_ZONE_CALL_A_BIKE.csv', sep = ";", decimal = ",")

#%% merge with dat_stations to get start/end_station_name column
dat_stations = (dat_stations
                .merge(dat_rental_zone[['RENTAL_ZONE_HAL_ID', 'NAME']], 
                              left_on='start_station_id', 
                              right_on = 'RENTAL_ZONE_HAL_ID')
                .rename(columns = {'NAME': 'start_station_name'})
                .drop(columns = ["RENTAL_ZONE_HAL_ID", "start_station_id"])
                .merge(dat_rental_zone[['RENTAL_ZONE_HAL_ID', 'NAME']], 
                       left_on='end_station_id', 
                       right_on = 'RENTAL_ZONE_HAL_ID')
                .rename(columns = {'NAME': 'end_station_name'})
                .drop(columns = ["RENTAL_ZONE_HAL_ID", "end_station_id"])
                )

#%% calculate number of trips for each station pair
dat_stations = (dat_stations.groupby(['start_station_name', 'end_station_name'])
                .count()
                .reset_index()
                .sort_values('datetime_from', ascending = False)
                .rename(columns={'datetime_from': 'n'}))
dat_stations.head()

#%% plot share of obs
dat_stations['share_of_obs'] = np.cumsum(dat_stations.n, axis = 0) / sum(dat_stations.n)
plt.bar(range(len(dat_stations)), dat_stations.share_of_obs)
plt.xlabel("number of unique station pairs")
plt.ylabel("share of observations")
plt.show()

# %% data for plot
dat_plot = (dat_stations
            .pivot(index = 'end_station_name', columns = 'start_station_name', values='n')
            .fillna(value=0))
dat_plot.head()

# %% plot
fig = px.imshow(dat_plot,
                labels = dict(x = "start", y = "end", color = "trips"),
                color_continuous_scale='Blues',
                aspect="auto",
                title = "Number of trips by start and end station")
fig.update_xaxes(showticklabels=False)
fig.update_yaxes(showticklabels=False)
fig.show()
fig.write_html("./plots/heatmap_trips.html")

#%% save data

dat_plot.to_csv("./plots/data/trips_heatmap/dat_trips_heatmap.csv",
                index=True)
