import os
import glob
import numpy as np
import shutil
from datetime import datetime, timedelta
from fmiopendata.wfs import download_stored_query


def download_forecast(date, start_time, end_time, area):
    print(f"\nDownloading forecast data for {area} on {date}")
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

    # Create a folder to store the forecast data
    if not os.path.exists(f"./forecasts/{area}"):
        os.makedirs(f"./forecasts/{area}")

    # Extract the day, month, and year from the date
    day, month, year = date.day, date.month, date.year
    # Create new folder or delete all previous /forecasts/DDMM files
    folder = f"./forecasts/{area}/d{day:02d}m{month:02d}y{year}"
    if not os.path.exists(folder):
        os.makedirs(folder)
    else:
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (file_path, e))

    # Iterate over each hour in the specified time range
    current_time = start_time
    while current_time < end_time:
        next_time = current_time + timedelta(hours=1)
        start_time_str = current_time.strftime('%Y-%m-%dT%H:%M:%SZ')
        end_time_str = next_time.strftime('%Y-%m-%dT%H:%M:%SZ')

        model_data = download_stored_query("fmi::forecast::harmonie::surface::grid",
                                        args=["starttime=" + start_time_str,
                                                "endtime=" + end_time_str,
                                                "bbox=" + bbox])
        latest_run = max(model_data.data.keys())
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
        current_time = next_time

def precipitation_by_date(date, area):
    day, month, year = date.day, date.month, date.year
    folder = f"./forecasts/{area}/d{day:02d}m{month:02d}y{year}"
    precipitation = precipitation_by_folder(folder)
    return precipitation

def precipitation_by_folder(folder):
    print(f"\nProcessing day: {folder}")
    # List all CSV files in the directory
    csv_files = glob.glob(os.path.join(folder, '*.csv'))

    # Initialize a dictionary to store precipitation data by hour
    hourly_data = {}
    # Iterate over each CSV file
    for csv_file in csv_files:
        # Extract the hour from the filename
        filename = os.path.basename(csv_file)
        hour_str = filename.split('_')[2]  # Assuming the format is precipitation_data_YYYYMMDDTHHMMSS.csv
        hour = hour_str[:11]  # Extract YYYYMMDDTHH

        # Read the CSV data
        data = np.loadtxt(csv_file, delimiter=',')
        
        # Flatten the data to a 1D array
        flattened_data = data.flatten()
        
        # Convert the data to millimeters (assuming the data is already in kg/m², which is equivalent to mm)
        data_in_mm = flattened_data
        # Add the data to the corresponding hour in the dictionary
        if hour not in hourly_data:
            hourly_data[hour] = []
        hourly_data[hour].extend(data_in_mm)

    # Calculate the average precipitation for each hour
    hourly_averages = {hour: np.mean(values) for hour, values in hourly_data.items()}

    # Note: downloading the data for a given hour seems to give
    # the cumulative amount up to that point since the last model run

    # The raw data is in kg/m² (mm) per grid cell inside the bbox
    # calculating np.mean of the grid values gives the cumulative amount
    # up to that hour. To get the precipitation for the hour, we need to
    # calculate the difference between consecutive hours.

    # Print the average precipitation for each hour
    hourly_precipitation = []
    hour = sorted(hourly_averages.items())
    for i in range(1, len(hour)):
        # Calculate the difference in precipitation between consecutive hours
        hourly_precipitation.append(float(abs(hour[i][1] - hour[i-1][1])))

    return hourly_precipitation

def get_forecast_for_date(date, area):
    year, month, day = date.year, date.month, date.day
    start_time = datetime(year, month, day, 0, 0, 0)
    end_time = start_time + timedelta(days=1)
    # Check if the forecast data for the specified date exists
    if not os.path.exists(f"./forecasts/{area}/d{day:02d}m{month:02d}y{year}"):
        download_forecast(date, start_time, end_time, area)
    return precipitation_by_date(date, area)
