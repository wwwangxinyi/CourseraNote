from datetime import datetime
import numpy as np
import pandas as pd
import mplleaflet
import matplotlib.pyplot as plt


def leaflet_plot_stations(binsize, hashid):

    df = pd.read_csv('data/C2A2_data/BinSize_d{}.csv'.format(binsize))

    station_locations_by_hash = df[df['hash'] == hashid]

    lons = station_locations_by_hash['LONGITUDE'].tolist()
    lats = station_locations_by_hash['LATITUDE'].tolist()

    plt.figure(figsize=(8, 8))

    plt.scatter(lons, lats, c='r', alpha=0.7, s=200)

    return mplleaflet.display()

# leaflet_plot_stations(400,'fb441e62df2d58994928907a91895ec62c2c42e6cd075c2700843b89')


records = pd.read_csv(
    'data/C2A2_data/BinnedCsvs_d400/fb441e62df2d58994928907a91895ec62c2c42e6cd075c2700843b89.csv')
records['Date'] = records['Date'].astype('datetime64[D]')
records['Year'] = records['Date'].dt.year
records['Month'] = records['Date'].dt.month
records['Day'] = records['Date'].dt.day
records['Data_Value'] = records['Data_Value']/10
records2015 = records[records['Year'] == 2015]
d1 = datetime(2015, 1, 1)
records2015['delta'] = (records2015['Date'] - d1).dt.days + 1
# records2015
records = records[~((records['Month'] == 2) & (records['Day'] == 29))]
records = records[~(records['Year'] == 2015)]
Hrecords = records[records['Element'] == 'TMAX'].drop(
    'Year', axis=1).groupby(['Month', 'Day']).mean()
Lrecords = records[records['Element'] == 'TMIN'].drop(
    'Year', axis=1).groupby(['Month', 'Day']).mean()

H2015 = records2015[records2015['Element'] == 'TMAX'].drop('Year', axis=1).groupby(
    ['Month', 'Day']).aggregate({'Data_Value': np.max, 'delta': np.mean})
L2015 = records2015[records2015['Element'] == 'TMIN'].drop('Year', axis=1).groupby(
    ['Month', 'Day']).aggregate({'Data_Value': np.min, 'delta': np.mean})
H2015.rename(columns={'Data_Value': 'Data_Value2015'}, inplace=True)
L2015.rename(columns={'Data_Value': 'Data_Value2015'}, inplace=True)

scatter_H = H2015.merge(Hrecords, left_index=True,
                        right_index=True, how='outer')
scatter_L = L2015.merge(Lrecords, left_index=True,
                        right_index=True, how='outer')

scatter_H = scatter_H[scatter_H['Data_Value2015'] > scatter_H['Data_Value']]
scatter_L = scatter_L[scatter_L['Data_Value2015'] < scatter_L['Data_Value']]

line_H = Hrecords['Data_Value'].tolist()
line_L = Lrecords['Data_Value'].tolist()

dates = np.arange(365)

# data plot
fig = plt.figure(1, figsize=(16, 9))
plt.plot(dates, line_H, 'r', label="2005-2014 record high temp")
plt.plot(dates, line_L, 'b', label="2005-2014 record low temp")
plt.gca().fill_between(range(len(dates)), line_L, line_H, facecolor='red', alpha=0.2)
plt.scatter(scatter_H['delta'], scatter_H['Data_Value2015'], marker='^',
            s=15, c='red', label='2015 record high temp. above the 2005-2014 record')
plt.scatter(scatter_L['delta'], scatter_L['Data_Value2015'], marker='v',
            s=15, c='blue', label='2015 record low temp. below the 2005-2014 record')

plt.xlabel('Days of a year (exclude leap day)', fontsize=14)
plt.ylabel("Temperature in degree Celcius", fontsize=14)
plt.title('Record high & low temperatures by day of the year over the period 2005-2015', fontsize=20)
plt.suptitle(
    'Data recorded by stations in Ann Arbor, Michigan, United States', y=-.005, fontsize=14)
plt.legend(loc=4, frameon=False)
plt.show()
fig.savefig('temp_plot.png')
