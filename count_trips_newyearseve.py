#-----------------------------------------------------#
#- This script calculates how many people spent 
#- New Year's Eve on a Call-a-bike in each year
#- included in the dataset
#-----------------------------------------------------#

#%% libs
import matplotlib.pyplot as plt
import pandas as pd

#%% read data 
dat_trips = pd.read_csv('./data/biketrip_data.csv')

#%% transform columns to datetime objects
dat_trips.date_to = pd.to_datetime(dat_trips.date_to)
dat_trips.date_from = pd.to_datetime(dat_trips.date_from)
dat_trips.datetime_to = pd.to_datetime(dat_trips.datetime_to)
dat_trips.datetime_from = pd.to_datetime(dat_trips.datetime_from)

#%% drop superfluous column
names_predrop = dat_trips.columns
dat_trips = dat_trips.drop(labels = 'Unnamed: 0', axis = 1)
names_postdrop = dat_trips.columns
names_predrop.difference(names_postdrop)

#%% print df info to check for possible missing obs
dat_trips.info(show_counts=True)

#%% Identify those trips that end the day after they started!
dat_trips['is_midnight_owl'] = dat_trips.date_from < dat_trips.date_to

#%% subset rows of original df
dat_trips_midnight = dat_trips[dat_trips['is_midnight_owl']][['datetime_from', 'is_midnight_owl']]

#%% calculate auxiliary columns 
dat_trips_midnight['year'] = dat_trips_midnight.datetime_from.dt.year
dat_trips_midnight['month'] = dat_trips_midnight.datetime_from.dt.month
dat_trips_midnight['day'] = dat_trips_midnight.datetime_from.dt.day


#%% filter for those trips starting on new year's eve (and thus ending on Jan 1)
dat_trips_midnight['is_newyears_eve'] = (dat_trips_midnight['month'] == 12) & (dat_trips_midnight['day'] == 31)
dat_trips_newyearseve = dat_trips_midnight.loc[dat_trips_midnight.is_newyears_eve, :]

#%% count relative occurence of new year's eve trips
print(len(dat_trips_newyearseve))
print(len(dat_trips))
print(len(dat_trips_newyearseve)/len(dat_trips)* 100)


#%% count by year
dat_trips_newyearseve_count = dat_trips_newyearseve.rename(columns = {'datetime_from': 'n_trips'}).groupby('year')[['n_trips']].count()

# %% export result as markdown table
dat_trips_newyearseve_count.to_markdown(buf = './tables/n_trips_newyearseve.md', 
                                              index = True)
