import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.pyplot import xlabel, ylabel, title
from scipy import stats

"""
Question 1: What was the overall change in average pit stop time?
"""

pit_data = pd.read_csv('pit_stops.csv')
pit_race_id = pit_data[['raceId','milliseconds']]
pit_race_id_numpy = pit_race_id.to_numpy()

average_list = []
current_race_id = pit_race_id_numpy[0, 0]
pit_list = []
list_of_races = []
list_of_races.insert(0,pit_race_id_numpy[0,0])

# Loop through the numpy array
for i in range(len(pit_race_id_numpy)):
    race_id, milliseconds = pit_race_id_numpy[i]

    if race_id == current_race_id and milliseconds < 60000:
        pit_list.append(milliseconds)
    elif milliseconds > 60000:
        continue
    else:
        # Calculate average for the previous race and reset
        list_of_races.append(race_id)
        average_list.append(np.mean(pit_list))
        current_race_id = race_id
        pit_list = [milliseconds]

# Append the average for the last race
if pit_list:
    average_list.append(np.mean(pit_list))

average_list_seconds = np.divide(average_list,1000) # Convert to seconds
coefficients = np.polyfit(list_of_races, average_list_seconds, 1)  # 1 for a linear trendline
p = np.poly1d(coefficients)
plt.plot(list_of_races,p(average_list_seconds),"r--") # Plot trendline
plt.bar(list_of_races,average_list_seconds) # Plot graph
xlabel('Race ID')
ylabel('Time (s)')
title('Change in average pit stop times from 2011 to 2024')
plt.show()

m, b = coefficients
print(f"Question 1: Trendline equation: y = {m:.2f}x + {b:.2f}") # Print out trendline equation

"""
Question 2: What is the fastest pit stop time overall?
"""

fastest_race_time = np.min(pit_race_id_numpy[:,1]) / 1000 # Convert to seconds

print("Question 2: The fastest pit stop time from 2011 to 2024 was " + str(fastest_race_time) + " seconds")

"""
Question 3: Which race ID had the fastest pit stop time?
"""

fastest_race_index = np.argmin(pit_race_id_numpy[:,1]) # Return index of the fastest race
fastest_race_id = pit_race_id_numpy[fastest_race_index,0]

print("Question 3: The race ID with the fastest pit stop is " + str(fastest_race_id))

"""
Question 4: What is the fastest race lap time recorded for a selected circuit?
"""
lap_time_data = pd.read_csv('lap_times.csv')
lap_time_array = lap_time_data[['raceId','driverId','milliseconds']].to_numpy()

lap_time_list = []

for i in range(len(lap_time_array)):
    raceId, driverId, milli = lap_time_array[i]
    if raceId == 1125: # race ID for the Chinese Grand Prix
        lap_time_list.append(milli)

fastest_lap_time = np.min(lap_time_list) / 1000 # Convert to seconds
print("Question 4: The fastest lap time for the Chinese Grand Prix is " + str(fastest_lap_time) + " seconds")

# china_dates_chrono = ['2004-09-26','2005-10-16','2006-10-01','2007-10-07','2008-10-19','2009-04-19','2010-04-18','2011-04-17','2012-04-15','2012-04-15','2013-04-14','2014-04-20','2015-04-12','2016-04-17','2017-04-09''2018-04-15','2019-04-14','2024-04-21']

"""
Question 5: How has average lap time changed over time for a selected circuit?
"""

races_data = pd.read_csv('races.csv')
races_array = races_data[['raceId','name','date']].to_numpy()

china_race_ids = []
china_dates = []

for i in range(len(races_array)):
    raceId, name, date = races_array[i]

    if name == "Chinese Grand Prix":
        china_race_ids.append(raceId)
        china_dates.append(date)

china_lap_list = []
average_CGP_time_list = []
current_race_id = None

for i in range(len(lap_time_array)):
    raceId, driverId, milli = lap_time_array[i]

    # Check if the race ID belongs to China races
    if raceId in china_race_ids:
        # If it's a new race ID, calculate average for the previous race ID and reset
        if raceId != current_race_id and china_lap_list:
            average_CGP_time_list.append(np.mean(china_lap_list))
            china_lap_list.clear()

        # Update the current race ID and add the lap time to the list
        current_race_id = raceId
        china_lap_list.append(milli)
    else:
        # If race ID is not in China races, finalize the current race's average
        if china_lap_list:
            average_CGP_time_list.append(np.mean(china_lap_list))
            china_lap_list.clear()
        current_race_id = None  # Reset current race ID

# Finalize average for the last race ID in case it was not added
if china_lap_list:
    average_CGP_time_list.append(np.mean(china_lap_list))

average_CGP_seconds = np.divide(average_CGP_time_list,1000) # Convert to seconds

plt.bar(china_dates,average_CGP_seconds)
plt.xlabel("Date", fontsize=10 )
plt.ylabel("Time (s)")
plt.xticks(fontsize=6)
plt.title("Change in average lap time for the Chinese Grand Prix")
plt.show()

"""
Question 6: Who is overall the best driver? (most wins)
"""

driver_data = pd.read_csv('driver_standings.csv')
driver_array = driver_data[['driverId','position']].to_numpy()

driver_winner_list = []

for i in range(len(driver_array)):
    driverId, position = driver_array[i]

    # Loop through array and count append the driver ID each time they finish in position 1
    if position == 1:
        driver_winner_list.append(driverId)
    else:
        continue

driver_winner = stats.mode(driver_winner_list) # Return the mode and number of occurrences using SciPy
print(driver_winner)

# Evaluate the print statement visually
print("Question 6: The driver with the most wins ever is Driver ID 1 with 125 wins. This is Lewis Hamilton")

"""
Question 7: What team has the most wins?
"""

constructor_data = pd.read_csv('constructor_standings.csv')
constructor_array = constructor_data[['constructorId','position']].to_numpy()

constructor_win_list = []

for i in range(len(constructor_array)):
    constructorId, position = constructor_array[i]

    # Loop through array and count append the constructor ID each time they finish in position 1
    if position == 1:
        constructor_win_list.append(constructorId)
    else:
        continue

constructor_winner = stats.mode(constructor_win_list) # Return the mode and number of occurrences using SciPy
print(constructor_winner)

# Evaluate the print statement visually
print("The constructor with the most wins is Constructor ID 6 with 234 wins. This is Ferrari")





















