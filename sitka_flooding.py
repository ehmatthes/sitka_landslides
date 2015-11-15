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
cum_rainfall.append(rainfall[0])
for new_precip in rainfall[1:]:
    cum_rf = round((cum_rainfall[-1] + new_precip), 2)
    cum_rainfall.append(cum_rf)
    
# Rainfall readings accumulate within the hour. So subtract that hour's previous
#  reading to get adjusted readings.
print("Adjusting cumulative rainfall...")
adj_cum_rainfall = []
for index, cum_rf in enumerate(cum_rainfall):
    ts = timestamps[index]
    if index > 0:
        if ts.strftime("%I") == timestamps[index-1].strftime("%I"):
            # Need to adjust; do so, then continue loop.
            adj_cum_rf = round((cum_rf - rainfall[index-1]), 2)
            adj_cum_rainfall.append(adj_cum_rf)
            print(ts.strftime("%I:%M %p"), cum_rf, adj_cum_rf)
            continue
    # No need to adjust.
    adj_cum_rainfall.append(cum_rf)
    print(ts.strftime("%I:%M %p"), cum_rf)



# for index, ts, rf in enumerate(zip(timestamps, rainfall)):
#     print('yes')


# From scraping loop:
# if timestamps:
#     if current_timestamp.strftime("%I") == timestamps[-1].strftime("%I"):
#         new_precip -= rainfall[-1]

print("\nAll data:")
for data in zip(timestamps, rainfall, cum_rainfall, adj_cum_rainfall):
    print(data[0].strftime("%I:%M %p"), round(data[1], 2), round(data[2], 2), round(data[3], 2))

sys.exit()

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
