#%% libs
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns

#%% read data 
dat_trips = pd.read_csv('./data/biketrip_data.csv')

#%% transform column to datetime 
dat_trips['datetime'] = pd.to_datetime(dat_trips.datetime_from)

#%% drop all columns except datetime 
dat_trips = dat_trips[['datetime']]
dat_trips.info(show_counts=True)

#%% add columns
dat_trips['weekday'] = dat_trips.datetime.dt.strftime('%A')
dat_trips['hour'] = dat_trips.datetime.dt.hour
dat_trips['min'] = dat_trips.datetime.dt.minute

#%% calculate intervals
def calculate_interval(df, minutes_in_interval):
    return(df['hour'] + np.floor(df['min']/minutes_in_interval)/(60/minutes_in_interval))
dat_trips['hour_interval'] =  calculate_interval(dat_trips, 60)

#%% compare hourly and 60 minute-interval trip count -> should be the same!!
dat_plot_hour_interval = dat_trips.groupby('hour_interval').count()[['datetime']]
dat_plot_hour = dat_trips.groupby('hour').count()[['datetime']]
plt.plot(dat_plot_hour.index, dat_plot_hour.datetime, label = 'hour')
plt.plot(dat_plot_hour_interval.index, dat_plot_hour_interval.datetime, label = 'interval_60')
plt.legend(loc = 'upper left')
plt.xticks(ticks = range(0,24, 2), 
           labels = list(map(lambda x: str(x) + ':00', 
                    range(0, 24, 2))),
            rotation = 30)
plt.title('Hourly bike rides')

#%% plot trips in finer minute windows, grouped by weekdays

# calculate interval in minutes by which to count trips
dat_trips['interval'] =  calculate_interval(dat_trips, 15)

# data for plot -> possible in one step?
dat_plot = dat_trips.groupby('weekday')['interval'].value_counts().sort_index().reset_index()
dat_plot = dat_plot.pivot(index='interval',
                                 columns='weekday', 
                                 values='count')
# reorder columns
dat_plot = dat_plot[['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']]

# plot and color setting
plt.style.use('seaborn')
my_cmap = sns.color_palette(palette="flare", n_colors = 7, as_cmap=True)

# actual plot
ax = dat_plot.plot(colormap=my_cmap,
                   title = "Number of bike rides by time of day",
                   figsize=(15,8))

# set xticks, labels, legend
ax.set_xticks(ticks = range(0,24, 1), 
              labels = list(map(lambda x: str(x) + ':00', 
                            range(0, 24, 1))),
              rotation = 0)
ax.set_xlabel("")
ax.legend(title = None, loc = 'upper left')

# save plot
plt.savefig('./plots/trips_by_weekday.png')

# %% save plot data to file
dat_plot.to_csv("./plots/data/trips_weekday/dat_trips_by_weekday.csv",
                index=True)
