"""
Plot cumulative rainfall against river stage level.
Look for correlation between rainfall intensity, river stage response,
  and whether mudslides occurred.
Also look at windspeed and gusts, and any other relevant factors that can
  define a predictive signature.
What factor comes first? Probably wind?
"""

"""
Examining 8/18/2015 event.
2.65 in total rainfall for the day, from wunderground.
So, seems some issue with incremental amounts.
"""

import csv, sys
from datetime import datetime

from matplotlib import pyplot as plt

# Get dates and incremental rainfall from file.
filename = 'pasi_precip_081815.csv'
with open(filename) as f:
    reader = csv.reader(f)
    header_row = next(reader)
    
    # for index, item in enumerate(header_row):
    #     print(index, item)

    timestamps, rainfall = [], []
    cum_rainfall = []
    
    for row in reader:
        # current_timestamp = datetime.strptime(row[0], "%Y-%m-%d")
        try:
            current_timestamp = datetime.strptime(row[0], "%I:%M %p")
            new_precip = round((float(row[9])), 2)
        except ValueError:
            pass#print("Error, data:", row)
        else:
            timestamps.append(current_timestamp)
            rainfall.append(new_precip)


cum_rainfall = []
for index, new_precip in enumerate(rainfall):
    if index == 0:
        cum_rainfall.append(new_precip)
        continue
    cum_rf = round((cum_rainfall[-1] + new_precip), 2)
    if timestamps[index].strftime("%I") == timestamps[index-1].strftime("%I"):
        print('adjusting')
        cum_rf -= round(rainfall[index-1], 2)
    cum_rainfall.append(round(cum_rf, 2))

# print("\nAll data:")
# for data in zip(timestamps, rainfall, cum_rainfall):
#     print(data[0].strftime("%I:%M %p"), data[1], data[2])

# Plot data.
fig = plt.figure(dpi=128, figsize=(10, 6))
# Plot the incremental rainfall.
plt.plot(timestamps, rainfall, c='blue')
# Plot the cumulative rainfall.
plt.plot(timestamps, cum_rainfall, c='red')

# Format plot.
plt.title("New rainfall, August 18 2015", fontsize=24)
plt.xlabel('', fontsize=16)
fig.autofmt_xdate()
plt.ylabel("Rainfall (in)", fontsize=16)
plt.tick_params(axis='both', which='major', labelsize=16)

plt.show()


# Add windspeed plot beneath this.
# Add moving 3-hour rainfall total?
