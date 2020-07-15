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
fig.tight_layout(pad=7)


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
    # axs[0].set_xticks()
    axs[0].set_yticks(np.arange(-30, 40, 5))

    axs[0].set_xlabel("Years", fontsize=10)
    axs[0].set_ylabel("°C", fontsize=10)
    #axs[0].legend(loc="upper right")

    # Filling between max and min lines
    axs[0].fill_between(data_max_plot1.index,
                        data_min_plot1['Data_Value'], data_max_plot1['Data_Value'],
                        facecolor='blue', alpha=0.25)

def create_plot2():
    data_max_plot2 = data_max['2015-01-01':'2015-12-31']
    data_min_plot2 = data_min['2015-01-01':'2015-12-31']
    data_range_max = list(map(pd.to_datetime, data_max_plot2.index))
    data_range_min = list(map(pd.to_datetime, data_min_plot2.index))


    axs[1].plot(data_range_max, data_max_plot2['Data_Value'], color='red', label="maximum", linewidth=0.5)
    axs[1].plot(data_range_min, data_min_plot2['Data_Value'], color='blue', label="minimum", linewidth=0.5)

    # Creating title
    axs[1].set_title("Maximum and minimum temperatures per day in 2015.", fontsize=10)
    fig = plt.gcf()
    fig.set_size_inches(7, 4)
    axs[1].set_xticks(data_max_plot2.index[::31])
    axs[1].set_xticklabels(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul',
                       'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
    axs[1].set_yticks(np.arange(-30, 40, 5))

    axs[1].set_xlabel("Years", fontsize=10)
    axs[1].set_ylabel("°C", fontsize=10)
    axs[1].legend(loc="upper right")

    # Filling between max and min lines
    axs[1].fill_between(data_max_plot2.index,
                        data_min_plot2['Data_Value'], data_max_plot2['Data_Value'],
                        facecolor='blue', alpha=0.25)
    def create_scatter():
        scatter_max = data[data['Element'] == "TMAX"].groupby('Date').max().copy()
        scatter_min = data[data['Element'] == "TMIN"].groupby('Date').min().copy()
        scatter_max = scatter_max['2005-01-01':'2014-12-31']
        scatter_min = scatter_min['2005-01-01':'2014-12-31']

        scatter_max['Data_Value'] /= 10
        scatter_min['Data_Value'] /= 10

        scatter_max.index = pd.to_datetime(scatter_max.index)
        scatter_min.index = pd.to_datetime(scatter_max.index)
        pd.set_option('display.max_rows', None)

        scatter_max = scatter_max.loc[scatter_max.groupby([scatter_max.index.month, scatter_max.index.day])['Data_Value'].idxmax()]
        scatter_min = scatter_min.loc[scatter_min.groupby([scatter_min.index.month, scatter_min.index.day])['Data_Value'].idxmin()]

        #scatter_max.index.map(change_year)
        print(scatter_max.index)
        #axs[0].scatter(scatter_max.index, scatter_max['Data_Value'], marker='o')
        #axs[0].scatter(scatter_min.index, scatter_min['Data_Value'], marker='o')





    create_scatter()

create_plot()
create_plot2()

#plt.show()