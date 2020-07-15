import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import datetime

#Loading data
data = pd.read_csv("fb441e62df2d58994928907a91895ec62c2c42e6cd075c2700843b89.csv")
data_max = data[data['Element'] == "TMAX"].groupby('Date').max()
data_min = data[data['Element'] == "TMIN"].groupby('Date').min()
data_max['Data_Value'] = data_max['Data_Value']/10
data_min['Data_Value'] = data_min['Data_Value']/10

# Removing leapdays i.e 29/02
for i in range(2005, 2015):
    try:
        data_max.drop(data_max[data_max.index == '{}-02-29'.format(i)].index, inplace=True)
        data_min.drop(data_min[data_min.index == '{}-02-29'.format(i)].index, inplace=True)
    except:
        pass

fig, axs = plt.subplots(2, figsize=(8, 7))
fig.tight_layout(pad=5)

def create_plot():
    data_max_plot1 = data_max['2005-01-01':'2014-12-31']
    data_min_plot1 = data_min['2005-01-01':'2014-12-31']

    data_range_max = list(map(pd.to_datetime, data_max_plot1.index))
    data_range_min = list(map(pd.to_datetime, data_min_plot1.index))

    axs[0].plot(data_range_max, data_max_plot1['Data_Value'], color='red', label="maximum", linewidth=0.5)
    axs[0].plot(data_range_min, data_min_plot1['Data_Value'], color='blue', label="minimum", linewidth=0.5)

    # Creating title
    axs[0].set_title("Maximum and minimum temperatures per day in Ann Arbor, Michigan.", fontsize=10)
    fig = plt.gcf()
    fig.set_size_inches(7, 4)
    axs[0].set_yticks(np.arange(-30, 40, 5))

    axs[0].set_xlabel("Years", fontsize=10)
    axs[0].set_ylabel("°C", fontsize=10)
    axs[0].legend(loc="upper right", fontsize=6)

    # Filling between max and min lines
    axs[0].fill_between(data_max_plot1.index,
                        data_min_plot1['Data_Value'], data_max_plot1['Data_Value'],
                        facecolor='blue', alpha=0.25)
def create_plot2():
    scatter_max = data[data['Element'] == "TMAX"].groupby('Date').max()
    scatter_min = data[data['Element'] == "TMIN"].groupby('Date').min()
    scatter_max = scatter_max['2005-01-01':'2014-12-31']
    scatter_min = scatter_min['2005-01-01':'2014-12-31']
    for i in range(2005, 2015):
        try:
            scatter_max.drop(scatter_max[scatter_max.index == '{}-02-29'.format(i)].index, inplace=True)
            scatter_min.drop(scatter_min[scatter_min.index == '{}-02-29'.format(i)].index, inplace=True)
        except:
            pass
    scatter_max['Data_Value'] /= 10
    scatter_min['Data_Value'] /= 10

    scatter_max.index = pd.to_datetime(scatter_max.index)
    scatter_min.index = pd.to_datetime(scatter_max.index)

    scatter_max = scatter_max.loc[
        scatter_max.groupby([scatter_max.index.month, scatter_max.index.day])['Data_Value'].idxmax()]
    scatter_min = scatter_min.loc[
        scatter_min.groupby([scatter_min.index.month, scatter_min.index.day])['Data_Value'].idxmin()]

    # Setting index year to 2015
    scatter_max.index = pd.DatetimeIndex(scatter_max.index)
    scatter_max.index = scatter_max.index + pd.DateOffset(year=2015)
    scatter_min.index = pd.DatetimeIndex(scatter_min.index)
    scatter_min.index = scatter_min.index + pd.DateOffset(year=2015)

    axs[1].plot(scatter_max.index, scatter_max['Data_Value'], color='gray', label="Temperature range 2005-2014", linewidth=0.5)
    axs[1].plot(scatter_max.index, scatter_min['Data_Value'], color='gray', linewidth=0.5)
    axs[1].fill_between(scatter_max.index,
                        scatter_min['Data_Value'], scatter_max['Data_Value'],
                        facecolor='blue', alpha=0.25)
    axs[1].set_xticks(scatter_max.index[::31])
    axs[1].set_xticklabels(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul',
                            'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])

    # 2015 data scatter
    data_2015_max = data_max['2015-01-01':'2015-12-31']
    data_2015_min = data_min['2015-01-01':'2015-12-31']

    data_2015_max.index = pd.to_datetime(data_2015_max.index)
    data_2015_min.index = pd.to_datetime(data_2015_min.index)

    data_2015_max = data_2015_max[data_2015_max['Data_Value'] > scatter_max['Data_Value']]
    data_2015_min = data_2015_min[data_2015_min['Data_Value'] < scatter_min['Data_Value']]

    axs[1].set_title("Higher and lower temperatures in 2015 related to 2004 untill 2014")
    axs[1].scatter(data_2015_max.index, data_2015_max['Data_Value'], color='red', s=1, label="Higher in 2015")
    axs[1].scatter(data_2015_min.index, data_2015_min['Data_Value'], color='blue', s=1, label="Lower in 2015")
    axs[1].legend(loc="lower right", fontsize=6)
    axs[1].set_xlabel("Months", fontsize=10)
    axs[1].set_yticks(np.arange(-30, 40, 5))
    axs[1].set_ylabel("°C", fontsize=10)


create_plot()
create_plot2()

plt.show()