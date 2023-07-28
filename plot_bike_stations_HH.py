#%% libs
import geopandas as gpd
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import shapely as sh
plt.style.use('seaborn')

#%% PLZ shape data
path_data = './data/plz/plz-5stellig.shp'
plz_shape_df = gpd.read_file(path_data, dtype={'plz': str})
plz_shape_df.plot(color='orange', alpha=0.8)


#%% PLZ by Bundesland
url_pzl_info = 'https://downloads.suche-postleitzahl.org/v2/public/zuordnung_plz_ort.csv'
plz_info = pd.read_csv(url_pzl_info, dtype={'plz': str})
plz_info_hh = plz_info[plz_info.bundesland == 'Hamburg']

#%% filter plz_shapes for Hamburg only
plz_shape_df_hh = plz_shape_df[plz_shape_df.plz.isin(plz_info_hh.plz)]
plz_shape_df_hh.plot()

# %% filter "mainland" Hamburg
id_mainland = []
cutoff_x = 9.5
cutoff_y = 53.8
for poly in plz_shape_df_hh.geometry:
    # get coordinates of polygon
    coords_poly = sh.get_coordinates(poly)

    # check x coords
    check_x = all(coords_poly[:, 0] > cutoff_x) 
    # check y coords
    check_y = all(coords_poly[:, 1] < cutoff_y)

    # update id 
    if check_x & check_y :
        id_mainland.append(True)
    else:
        id_mainland.append(False)
sum(id_mainland)/len(id_mainland)

plz_shape_df_hh = plz_shape_df_hh[id_mainland]

#%% load bike station locations

dat_rental_zone = pd.read_csv('./data/OPENDATA_RENTAL_ZONE_CALL_A_BIKE.csv', sep = ";", decimal = ",")
dat_rental_zone_hh = dat_rental_zone[dat_rental_zone.CITY == 'Hamburg']
dat_rental_zone_hh = dat_rental_zone_hh[['NAME', 'LATITUDE', 'LONGITUDE']]


#%% plot bike station locations
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


plt.savefig('./plots/bike_stations_HH.png')


# %% save plot data to file

plz_shape_df_hh.to_file("./plots/data/bike_stations_HH/plz_shape_df_hh.shp", 
                       index=False)
dat_rental_zone_hh.to_csv("./plots/data/bike_stations_HH/dat_rental_zone_hh.csv",
                          index=False)
