import os
import glob
import numpy as np
import shutil
from datetime import datetime, timedelta
from fmiopendata.wfs import download_stored_query


def download_forecast(date, start_time, end_time, area):
    print(f"\nDownloading forecast data for {area} on {date}")
    # Check if date is currennt date, then set to current time of day
    if date == datetime.now().date():
        start_time = datetime.now()
    #convert to UTC
    start_time = start_time - timedelta(hours=3)
    end_time = end_time - timedelta(hours=3)

    # bounding boxes from https://boundingbox.klokantech.com/
    # pirkkola $$c(E 24°55'30"--E 25°00'07"/N 60°13'53"--N 60°11'33")
    bounding_boxes = {
        "Hietaniemi": "24.76639,60.21111,24.86083,60.34444",
        "Paloheinä": "24.97083,60.26278,24.90361,60.29667",
        "Pirkkola": "24.97083,60.26278,24.90361,60.29667"
    }
    bbox = bounding_boxes[area]

    # Extract the day, month, and year from the date
    day, month, year = date.day, date.month, date.year
    # Create new folder
    folder = f"./forecasts/{area}/d{day:02d}m{month:02d}y{year}"
    if not os.path.exists(folder):
        os.makedirs(folder)

    # Check which hours have already been downloaded by parsing filenames
    downloaded_hours = set()
    for filename in os.listdir(folder):
        if filename.startswith("precipitation_data_"):
            datetime_str = filename.split("precipitation_data_")[1].split(".")[0]
            file_datetime = datetime.strptime(datetime_str, '%Y%m%dT%H%M%S')
            downloaded_hours.add(file_datetime)

    print(f"Downloaded hours: {sorted(downloaded_hours)}")

    # Get the current time
    current_time = datetime.utcnow()

    # Iterate over each hour in the specified time range
    current_time = start_time
    while current_time < end_time:
        if current_time not in downloaded_hours:
            next_time = current_time + timedelta(hours=1)
            start_time_str = current_time.strftime('%Y-%m-%dT%H:%M:%SZ')
            end_time_str = next_time.strftime('%Y-%m-%dT%H:%M:%SZ')

            model_data = download_stored_query("fmi::forecast::harmonie::surface::grid",
                                               args=["starttime=" + start_time_str,
                                                     "endtime=" + end_time_str,
                                                     "bbox=" + bbox])
            # Check if the download was successful
            try:
                latest_run = max(model_data.data.keys())
            except Exception:
                current_time = next_time
                continue

            data = model_data.data[latest_run]
            # This will download the data to a temporary file, parse the data and delete the file
            data.parse(delete=True)

            valid_times = data.data.keys()

            target_level = 10
            target_dataset_name = "surface precipitation amount, rain, convective"

            for time_step in valid_times:
                datasets = data.data[time_step][target_level]
                if target_dataset_name in datasets:
                    unit = datasets[target_dataset_name]["units"]
                    data_array = datasets[target_dataset_name]["data"]  # Numpy array of the actual data
                    print(f"Time: {time_step}, Level: {target_level}, dataset name: {target_dataset_name}, data unit: {unit}")
                    # Write out to a file named with the current time step
                    filename = f"{folder}/precipitation_data_{time_step.strftime('%Y%m%dT%H%M%S')}.csv"
                    np.savetxt(filename, data_array, delimiter=",")

        # Move to the next hour
        current_time += timedelta(hours=1)

def precipitation_by_date(date, area):
    day, month, year = date.day, date.month, date.year
    folder = f"./forecasts/{area}/d{day:02d}m{month:02d}y{year}"
    precipitation = precipitation_by_folder(folder, date)
    return precipitation

def precipitation_by_folder(folder, date):
    print(f"\nProcessing day: {folder}")
    # List all CSV files in the directory
    csv_files = glob.glob(os.path.join(folder, '*.csv'))
    if len(csv_files) == 0:
        return ["NaN"] * 24

    # Initialize a dictionary to store precipitation data by hour
    hourly_data = []

    # Iterate over each CSV file
    for csv_file in csv_files:
        filename = os.path.basename(csv_file)
        print(f"Processing file: {csv_file}")
        # Extract the hour from the filename
        if filename.startswith("precipitation_data_"):
            datetime_str = filename.split("precipitation_data_")[1].split(".")[0]
            file_datetime = datetime.strptime(datetime_str, '%Y%m%dT%H%M%S')
            print(f"Data {file_datetime}")

        # Read the CSV data
        data = np.loadtxt(csv_file, delimiter=',')
        
        # Flatten the data to a 1D array
        flattened_data = data.flatten()
        
        # Convert the data to millimeters (assuming the data is already in kg/m², which is equivalent to mm)
        data_in_mm = flattened_data
        # Add the data to the corresponding hour in the dictionary
        hourly_data.append((float(abs(np.mean(data_in_mm))), file_datetime))
    
    # Note: downloading the data for a given hour seems to give
    # the cumulative amount up to that point since the last model run

    # The raw data is in kg/m² (mm) per grid cell inside the bbox
    # calculating np.mean of the grid values gives the cumulative amount
    # up to that hour. To get the precipitation for the hour, we need to
    # calculate the difference between consecutive hours.

    # Print the average precipitation for each hour
    day, month, year = date.day, date.month, date.year

    # needed hours from day-1, 21:00 till day: 21:00, '%Y%m%dT%H%M%S'
    needed_hours = [datetime(year, month, day, i, 0, 0) - timedelta(hours=3) for i in range(24)]
    needed_hours += [datetime(year, month, day, 21, 0, 0)]
    needed_hours = [hour.strftime('%Y%m%dT%H%M%S') for hour in needed_hours]
    print(f"Needed hours: {needed_hours}")

    # Calculate the hourly precipitation
    hourly_precipitation = {}
    for hour in needed_hours:
        found = False
        for data, file_datetime in hourly_data:
            if hour == file_datetime.strftime('%Y%m%dT%H%M%S'):
                hourly_precipitation[hour] = data
                found = True
                break
        print(f"Hour: {hour} found in data: {found}")
        if not found:
            hourly_precipitation[hour] = "NaN"

    # Calculate the difference between consecutive hours
    hourly_precipitation_diff = []
    sorted_hours = sorted(hourly_precipitation.items())
    for i in range(1, len(sorted_hours)):
        current_data = sorted_hours[i][1]
        previous_data = sorted_hours[i - 1][1]
        if current_data == "NaN" or previous_data == "NaN":
            hourly_precipitation_diff.append("NaN")
        else:
            hourly_precipitation_diff.append(float(abs(current_data - previous_data)))

    return hourly_precipitation_diff


def get_forecast_for_date(date, area):
    year, month, day = date.year, date.month, date.day
    start_time = datetime(year, month, day, 0, 0, 0)
    end_time = start_time + timedelta(days=1)
    # Check if the forecast data for the specified date exists
    if not os.path.exists(f"./forecasts/{area}/d{day:02d}m{month:02d}y{year}"):
        download_forecast(date, start_time, end_time, area)
    elif len(os.listdir(f"./forecasts/{area}/d{day:02d}m{month:02d}y{year}")) < 25:
        download_forecast(date, start_time, end_time, area)
    return precipitation_by_date(date, area)
