# This code reproduces the plot of bike trips by day of the week 
# by loading the required data that has been comitted to the repo
# and should thus be reproducible by anyone with access to the GitHub repo

#%% libs
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

#%% load plot data
dat_plot = pd.read_csv("./plots/data/trips_weekday/dat_trips_by_weekday.csv",
                       index_col='interval')

#%% plot

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

