# This code reproduces the plot of bike stations in HH
# by loading the required data from bespoke files

import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
plt.style.use('seaborn')

dir_dat_plot = './plots/data/bike_stations_HH/'
dat_rental_zone_hh = pd.read_csv(dir_dat_plot + 'dat_rental_zone_hh.csv')
plz_shape_df_hh = gpd.read_file(dir_dat_plot + 'plz_shape_df_hh.shp', dtype={'plz': str})

fig, ax = plt.subplots()

plz_shape_df_hh.plot(ax=ax, color='orange', alpha=0.8)

for index, row in dat_rental_zone_hh.iterrows():
    # ax.text(
    #     x=row['LATITUDE'], 
    #     # Add small shift to avoid overlap with point.
    #     y=row['LONGITUDE'] + 0.08, 
    #     s=row['NAME'], 
    #     fontsize=1,
    #     ha='center', 
    # )
    ax.plot(
        row['LATITUDE'], 
        row['LONGITUDE'], 
        marker='o',
        markersize = 3.0,
        c='black', 
        alpha=0.5
    )

ax.set(
    title='Bike stations in Hamburg', 
    aspect=1.3
    );
ax.xaxis.set_visible(False)
ax.yaxis.set_visible(False)

