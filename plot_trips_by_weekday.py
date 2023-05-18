#%% libs
import matplotlib.pyplot as plt
import pandas as pd

#%% read data 
dat_trips = pd.read_csv('./data/biketrip_data.csv')

#%% transform columns to datetime objects
dat_trips.date_to = pd.to_datetime(dat_trips.date_to, format = '%Y-%m-%d')
dat_trips.date_from = pd.to_datetime(dat_trips.date_from, format = '%Y-%m-%d')

#%% 
dat_trips.info(show_counts=True)

#%% add day of the week as column
dat_trips['weekday'] = dat_trips['date_from'].dt.strftime('%A')

#%% plot
dat_plot = dat_trips.groupby('weekday')['hour_from'].value_counts().sort_index().reset_index()
plot_colors =  {'Monday': 'darkred', 
                'Tuesday': 'chocolate',
                'Wednesday': 'coral',
                'Thursday': 'darkorchid',
                'Friday': 'royalblue',
                'Saturday': 'navy',
                'Sunday': 'black'}
plt.figure(figsize=(15,8))
for day in plot_colors.keys():
    plt.plot(dat_plot[dat_plot['weekday'] == day]['hour_from'], 
             dat_plot[dat_plot['weekday'] == day]['count'], 
             label = day,
             color = plot_colors[day],
             alpha = 1.0,
             linestyle = 'solid')   

plt.legend(loc = 'upper left')
plt.xticks(range(0,23, 3), 
           list(map(lambda x: str(x) + ':00', 
                    range(0, 23, 3))),
           rotation = 0)
plt.title('Number of bike rides by time of day')
plt.savefig('./plots/trips_by_weekday.png')


# %% save plot data to file
dat_plot.to_csv("./plots/data/trips_weekday/dat_trips_by_weekday.csv",
                          index=False)
# %%
