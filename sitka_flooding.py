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
    for row in reader:
        try:
            current_timestamp = datetime.strptime(row[0], "%I:%M %p")
            new_precip = round((float(row[9])), 2)
        except ValueError:
            pass#print("Error, data:", row)
        else:
            timestamps.append(current_timestamp)
            rainfall.append(new_precip)

# Rainfall measurements are cumulative within the hour.
#  So multiple readings in one hour need to take this into account.
cum_rainfall = []
for index, new_precip in enumerate(rainfall):
    if index == 0:
        cum_rainfall.append(new_precip)
        continue
    cum_rf = round((cum_rainfall[-1] + new_precip), 2)
    if timestamps[index].strftime("%I") == timestamps[index-1].strftime("%I"):
        # Multiple readings this hour; adjust, so don't double-count some readings.
        cum_rf -= round(rainfall[index-1], 2)
    cum_rainfall.append(round(cum_rf, 2))


# Get dates and wind data.
filename = 'pasi_precip_081815.csv'
with open(filename) as f:
    reader = csv.reader(f)
    header_row = next(reader)
    
    wind_timestamps, windspeeds, gusts = [], [], []
    for row in reader:
        try:
            wind_timestamp = datetime.strptime(row[0], "%I:%M %p")
            new_windspeed = row[7]
            if new_windspeed == 'Calm':
                new_windspeed = 0
            new_gust = row[8]
            if new_gust == '-':
                new_gust = 0
        except ValueError:
            print("Error, data:", row)
        else:
            wind_timestamps.append(wind_timestamp)
            windspeeds.append(float(new_windspeed))
            gusts.append(float(new_gust))


# Get dates and river level data.
filename = 'irva2_levels_082115.csv'
with open(filename) as f:
    reader = csv.reader(f)
    header_row = next(reader)
    
    irva_timestamps, irva_levels = [], []
    for row in reader:
        try:
            irva_timestamp = datetime.strptime(row[0], "%m/%d %H:%M")
            new_level = row[1].replace('ft', '')
            new_level = float(new_level)
        except ValueError:
            print("Error, data:", row)
        else:
            if irva_timestamp.strftime("%d") == '18':
                irva_timestamps.append(irva_timestamp)
                irva_levels.append(new_level)

# Set irva timestamps to match date of others.
for index, ts in enumerate(irva_timestamps[:]):
    base_ts = timestamps[0]
    irva_timestamps[index] = ts.replace(month=base_ts.month, day=base_ts.day)


# for ts, lv in zip(irva_timestamps, irva_levels):
#     print(ts.strftime("%H:%M"), lv)


# # Plot rainfall data.
# fig = plt.figure(0, dpi=128, figsize=(10, 6))
# # Plot the incremental rainfall.
# plt.plot(timestamps, rainfall, c='blue')
# # Plot the cumulative rainfall.
# plt.plot(timestamps, cum_rainfall, c='red')

# # Format plot.
# plt.title("New rainfall, August 18 2015", fontsize=24)
# plt.xlabel('', fontsize=16)
# fig.autofmt_xdate()
# plt.ylabel("Rainfall (in)", fontsize=16)
# plt.tick_params(axis='both', which='major', labelsize=16)

# # Plot wind data.
# fig = plt.figure(1, dpi=128, figsize=(10, 6))
# plt.plot(wind_timestamps, windspeeds, 'bo')
# plt.plot(wind_timestamps, gusts, 'ro')

# # Format plot.
# plt.title("Wind speed and gusts, August 18 2015", fontsize=24)
# plt.xlabel('', fontsize=16)
# fig.autofmt_xdate()
# plt.ylabel("Wind speed (mph)", fontsize=16)
# plt.tick_params(axis='both', which='major', labelsize=16)


# Plot rainfall and wind speeds as subplots.
# Plot rainfall data.
f, axarr = plt.subplots(3, sharex=True)
# Plot the incremental rainfall.
axarr[0].plot(timestamps, rainfall, c='blue')
# Plot the cumulative rainfall.
axarr[0].plot(timestamps, cum_rainfall, c='red')

# Format plot.
axarr[0].set_title("Rainfall and wind speeds, August 18 2015", fontsize=24)
f.autofmt_xdate()
axarr[0].set_ylabel("Rainfall (in)", fontsize=16)
axarr[0].tick_params(axis='both', which='major', labelsize=16)

# Plot wind data.
axarr[1].plot(wind_timestamps, windspeeds, 'bo')
axarr[1].plot(wind_timestamps, gusts, 'ro')
# Format plot.
axarr[1].set_ylabel("Wind speed (mph)", fontsize=16)

# Plot river level data.
axarr[2].plot(irva_timestamps, irva_levels, c='blue')
axarr[1].set_ylabel("Indian River level (ft)", fontsize=16)

# for tsr, tsw, tsi in zip(timestamps, wind_timestamps, irva_timestamps):
#     print(tsr.strftime("%m/%d/%Y %H:%M"), tsw.strftime("%m/%d/%Y %H:%M"), tsi.strftime("%m/%d/%Y %H:%M"))

plt.show()


# Add windspeed plot beneath this.
# Add moving 3-hour rainfall total?
