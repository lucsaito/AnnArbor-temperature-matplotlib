import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

#Loading data
data = pd.read_csv("fb441e62df2d58994928907a91895ec62c2c42e6cd075c2700843b89.csv")
data_max = data[data['Element'] == "TMAX"].groupby('Date').max()
data_min = data[data['Element'] == "TMIN"].groupby('Date').min()


data_max = data_max['2005-01-01':'2014-12-31']
data_min = data_min['2005-01-01':'2014-12-31']


data_max['Data_Value'] = data_max['Data_Value']/10
data_min['Data_Value'] = data_min['Data_Value']/10

# Removing leapdays i.e 29/02
for i in range(2005, 2015):
    try:
        data_max.drop(data_max[data_max.index == '{}-02-29'.format(i)].index, inplace=True)
        data_min.drop(data_min[data_min.index == '{}-02-29'.format(i)].index, inplace=True)
    except:
        pass

data_range_max = list(map(pd.to_datetime, data_max.index))
data_range_min = list(map(pd.to_datetime, data_min.index))

plt.plot(data_range_max, data_max['Data_Value'], color='red', label="maximum", linewidth=0.5)
plt.plot(data_range_min, data_min['Data_Value'], color='blue', label="minimum", linewidth=0.5)

# Creating title
plt.title("Maximum and minimum temperatures per day in Ann Arbor, Michigan.", fontsize=10)
fig = plt.gcf()
fig.set_size_inches(7, 3)
plt.xticks(fontsize=10)
plt.yticks(np.arange(-30, 40, 5) , fontsize=10)

plt.xlabel("Years")
plt.ylabel("°C")
plt.legend(loc="upper right")

# Filling between max and min lines
plt.gca().fill_between(data_max.index,
                      data_min['Data_Value'], data_max['Data_Value'],
                      facecolor='blue', alpha=0.25)

plt.show()



