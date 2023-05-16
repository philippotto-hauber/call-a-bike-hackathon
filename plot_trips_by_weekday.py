#%% libs
import matplotlib.pyplot as plt
import pandas as pd

#%% read data and transform
dat_trips = pd.read_csv('./data/biketrip_data.csv', 
                        nrows = 200000)

dat_trips.date_to = pd.to_datetime(dat_trips.date_to, format = '%Y-%m-%d')
dat_trips.date_from = pd.to_datetime(dat_trips.date_from, format = '%Y-%m-%d')

#%% Calculate those trips that end the day after they started!
dat_trips['is_midnight_owl'] = dat_trips.date_from < dat_trips.date_to

dat_trips_midnight = dat_trips[dat_trips['is_midnight_owl']]
dat_trips_midnight[['datetime_from', 'datetime_to']]
# try and do this in one step
#dat_trips.loc('is_midnight_owl', 'datetime_from') -> returns error

#%% plot number of trips per hour 

plt.plot(dat_trips['hour_from'].value_counts().sort_index())

#%% grouped count by day of the week
dat_trips['weekday'] = dat_trips['date_from'].apply(lambda x: x.strftime('%A'))
dat_plot = dat_trips.groupby('weekday')['hour_from'].value_counts().sort_index().reset_index()

for day in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']:
    plt.plot(dat_plot[dat_plot['weekday'] == day]['hour_from'], 
             dat_plot[dat_plot['weekday'] == day]['count'], 
             label = day)
    

plt.legend()
plt.show()

