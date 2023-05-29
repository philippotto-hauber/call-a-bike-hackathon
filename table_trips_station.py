#%% libs
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import dataframe_image as dfi

#%% load raw data

#%% select columns I need and transform to date format
dat_raw = pd.read_csv('./data/biketrip_data.csv')
dat_trips = dat_raw[['start_station_id', 
                   'end_station_id', 
                   'date_from']]
dat_trips['date'] = pd.to_datetime(dat_trips['date_from'])
del dat_raw
dat_trips.info(show_counts=True)

# %% get number of trips by start end combo in the whole sample
dat_stations = dat_trips.copy(deep=True)
dat_stations = dat_stations.drop(columns = ['date_from'])
dat_stations['n_trips'] = (dat_stations.groupby(['start_station_id', 
                                                 'end_station_id'])
                                        .transform('count')                                        
                            )
dat_stations = dat_stations.sort_values(by = 'n_trips', ascending = False).drop(columns = 'date').drop_duplicates()
dat_stations.head()

# %% add cumulative share of obs
dat_stations['cum_share'] = np.cumsum(dat_stations.n_trips, axis = 0) / sum(dat_stations.n_trips)

# %% select top 10 pairs of stations
dat_stations_top10 = dat_stations.head(10)

#%% define function

def get_share_missing(df_trips, id_start, id_end):
    # filter df containing all trips
    df_filter = (df_trips[(df_trips['start_station_id'] == id_start) & 
                        (df_trips['end_station_id'] == id_end)]
                [['date', 'date_from']]
                )
    
    #% group by date and count
    df_group = df_filter.groupby('date').count().rename(columns = {'date_from': 'n_trips'})

    #% get df of all dates in trips
    df_all_dates = pd.DataFrame(data={'date': pd.date_range(start=np.min(df_trips.date), 
                                                        end = np.max(df_trips.date))})
    
    # merge with grouped counts
    df_all_dates_merged = df_all_dates.merge(df_group, how= 'left', on = 'date')

    # set date as index
    df_all_dates_merged = df_all_dates_merged.set_index('date')

    # calculate share of nan's
    share_nan = df_all_dates_merged['n_trips'].isna().sum() / df_all_dates_merged.shape[0]
    return share_nan

#%% create share of NaNs for each combo in top 10
dat_stations_top10['share_NaN'] = 0.0
for i in dat_stations_top10.index:
    dat_stations_top10.loc[i, 'share_NaN'] = get_share_missing(dat_trips, 
                                                                dat_stations_top10.start_station_id[i],
                                                                dat_stations_top10.end_station_id[i]
                                                                )    
    
#%% replace station id with name
dat_rental_zone = pd.read_csv('./data/OPENDATA_RENTAL_ZONE_CALL_A_BIKE.csv', sep = ";", decimal = ",")

start_stations_id = dat_stations_top10['start_station_id']

dat_stations_top10 = (dat_stations_top10
                            .merge(dat_rental_zone[['RENTAL_ZONE_HAL_ID', 'NAME']], 
                                   how = "left",
                                   left_on='start_station_id', 
                                   right_on = 'RENTAL_ZONE_HAL_ID')
                            .rename(columns = {'NAME': 'start_station_name'})
                            .drop(columns = ["RENTAL_ZONE_HAL_ID"])
                            .merge(dat_rental_zone[['RENTAL_ZONE_HAL_ID', 'NAME']], 
                                   how = 'left',
                                   left_on='end_station_id', 
                                   right_on = 'RENTAL_ZONE_HAL_ID')
                            .rename(columns = {'NAME': 'end_station_name'})
                            .drop(columns = ["RENTAL_ZONE_HAL_ID"])
                            )

dat_stations_top10 = dat_stations_top10.drop(columns=['start_station_id', 'end_station_id'])
dat_stations_top10.head()


#%% clean up df before printing     

# rename columns
dat_stations_top10 = dat_stations_top10.rename(columns={'start_station_name': 'start',
                                                        'end_station_name': 'end'})
# rearrange columns
dat_stations_top10 = dat_stations_top10[['start', 'end', 'n_trips', 'cum_share', 'share_NaN']]

# round some columns for better readability
dat_stations_top10['cum_share'] = dat_stations_top10['cum_share'].round(3)
dat_stations_top10['share_NaN'] = dat_stations_top10['share_NaN'].round(3)

#%% print table
dfi.export(dat_stations_top10, './tables/top10_trips_stations.png')