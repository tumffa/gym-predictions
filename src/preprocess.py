import os
import pandas as pd


def process_hourly_data():
    # Directory containing the CSV files
    hours_csv_dir = './hourly_csv'

    # List to hold individual DataFrames
    hourly_dataframes = []

    # Iterate over all hourly CSV files in the directory
    for filename in os.listdir(hours_csv_dir):
        file_path = os.path.join(hours_csv_dir, filename)
        # Read the CSV file into a DataFrame
        df = pd.read_csv(file_path)
        # Append the DataFrame to the list
        hourly_dataframes.append(df)
    # Concatenate all hourly DataFrames in the list into a single DataFrame
    all_hourly_data_df = pd.concat(hourly_dataframes, ignore_index=True)
    # Sort the combined DataFrame by utctimestamp and area
    all_hourly_data_df = all_hourly_data_df.sort_values(by=['utctimestamp', 'area'])

    # Convert utctimestamp to datetime
    all_hourly_data_df['utctimestamp'] = pd.to_datetime(all_hourly_data_df['utctimestamp'])
    # Change column name to localtime
    all_hourly_data_df.rename(columns={'utctimestamp': 'localtime'}, inplace=True)
    # Convert to Finnish time
    all_hourly_data_df['localtime'] = all_hourly_data_df['localtime'] + pd.Timedelta(hours=3)
    # Format the localtime to 'YYYY-MM-DD HH:MM:SS'
    all_hourly_data_df['localtime'] = all_hourly_data_df['localtime'].dt.strftime('%Y-%m-%d %H:%M:%S')

    # Extract week of the year, month, day of the week, and hour of the day
    all_hourly_data_df['week_of_year'] = pd.to_datetime(all_hourly_data_df['localtime']).dt.isocalendar().week
    all_hourly_data_df['month'] = pd.to_datetime(all_hourly_data_df['localtime']).dt.month
    all_hourly_data_df['day_of_week'] = pd.to_datetime(all_hourly_data_df['localtime']).dt.weekday  # Monday=0, Sunday=6
    all_hourly_data_df['hour'] = pd.to_datetime(all_hourly_data_df['localtime']).dt.hour

    # Group by localtime and area and aggregate the total minutes, sets, and repetitions
    aggregated_df = all_hourly_data_df.groupby(['localtime', 'area']).agg(
        total_minutes=('usageMinutes', 'sum'),
        total_sets=('sets', 'sum'),
        total_reps=('repetitions', 'sum')
    ).reset_index()

    # Merge the week_of_year, month, day_of_week, and hour columns back into the aggregated DataFrame
    aggregated_df = pd.merge(aggregated_df, all_hourly_data_df[['localtime', 'week_of_year', 'month', 'day_of_week', 'hour']].drop_duplicates(), on='localtime')

    # Display size of the aggregated DataFrame
    print(f"Dataframe of total minutes per hour: {aggregated_df.shape}")

    return aggregated_df

def process_weather_data():
    # Weather data files
    weather_csv_folder = "./weather_data"
    weather_csv_files = ["espoo_weather.csv", "helsinkivantaa_weather.csv", "kumpula_weather.csv"]
    dataframes = []

    for weather_csv_file in weather_csv_files:
        weather_df = pd.read_csv(f"{weather_csv_folder}/{weather_csv_file}")

        # Convert the date and time columns to a single datetime column
        if "Aika [Paikallinen aika]" in weather_df.columns:
            weather_df['localtime'] = pd.to_datetime(weather_df[['Vuosi', 'Kuukausi', 'Päivä']].astype(str).agg('-'.join, axis=1) + ' ' + weather_df['Aika [Paikallinen aika]'])
            # Drop the original date and time columns
            weather_df.drop(columns=['Vuosi', 'Kuukausi', 'Päivä', 'Aika [Paikallinen aika]'], inplace=True)

        elif "Aika [UTC]" in weather_df.columns:
            weather_df['localtime'] = pd.to_datetime(weather_df[['Vuosi', 'Kuukausi', 'Päivä']].astype(str).agg('-'.join, axis=1) + ' ' + weather_df['Aika [UTC]'])
            # Convert to Finnish time
            weather_df['localtime'] = weather_df['localtime'] + pd.Timedelta(hours=3)
            # Drop the original date and time columns
            weather_df.drop(columns=['Vuosi', 'Kuukausi', 'Päivä', 'Aika [UTC]'], inplace=True)
        
        # Format the localtime to 'YYYY-MM-DD HH:MM:SS'
        weather_df['localtime'] = weather_df['localtime'].dt.strftime('%Y-%m-%d %H:%M:%S')

        # Rename the columns for clarity (helsinkivantaa doesn't have snow depth, thus if statement)
        if weather_csv_file == weather_csv_files[0] or weather_csv_file == weather_csv_files[2]:
            weather_df.rename(columns={
                'Havaintoasema': 'station',
                'Ilman lämpötila maksimi [°C]': 'temperature_c',
                'Sademäärä maksimi [mm]': 'precipitation_mm',
                "Lumensyvyys maksimi [cm]" : "snow_depth_cm"
            }, inplace=True)
        else:
            weather_df.rename(columns={
                'Havaintoasema': 'station',
                'Ylin lämpötila [°C]': 'temperature_c',
                'Tunnin sademäärä [mm]': 'precipitation_mm'
            }, inplace=True)

        # Convert values to numeric
        weather_df['temperature_c'] = pd.to_numeric(weather_df['temperature_c'], errors='coerce')
        weather_df['precipitation_mm'] = pd.to_numeric(weather_df['precipitation_mm'], errors='coerce')
        
        if 'snow_depth_cm' in weather_df.columns:
            weather_df['snow_depth_cm'] = pd.to_numeric(weather_df['snow_depth_cm'], errors='coerce')

        # Fill missing values by interpolating the closest 3 values
        weather_df['temperature_c'] = weather_df['temperature_c'].interpolate(method='nearest', limit_direction='both')
        weather_df['precipitation_mm'] = weather_df['precipitation_mm'].interpolate(method='nearest', limit_direction='both')

        if 'snow_depth_cm' in weather_df.columns:
            weather_df['snow_depth_cm'] = weather_df['snow_depth_cm'].interpolate(method='nearest', limit_direction='both')
            # Change all values of -1 to 0
            weather_df['snow_depth_cm'] = weather_df['snow_depth_cm'].replace(-1, 0)

        # Display size of the weather DataFrame
        print(f"Dataframe of weather data: {weather_df.shape}")

        name = weather_csv_file.split("_")[0]
        dataframes.append({"name": name, "data": weather_df})

    return dataframes

def combine_data(hourly_data, weather_data):
    # Make ./processed_data directory
    if not os.path.exists("./processed_data"):
        os.makedirs("./processed_data")

    # List to hold the combined dataframes
    training_dataframes = []

    # Merge dataframes
    for weather_df in weather_data:
        # drop the station column from weather_data
        weather_df['data'] = weather_df['data'].drop(columns=['station'])

        # merge the data
        combined_data = pd.merge(weather_df['data'], hourly_data, on='localtime')

        # Save the combined data to a new CSV file
        output_csv_file = f"./processed_data/training_data_{weather_df['name']}_weather.csv"
        combined_data.to_csv(output_csv_file, index=False)

        # Append the combined DataFrame to the list
        training_dataframes.append(combined_data)

        # Display the combined DataFrame
        print(f"Wrote combined data to {output_csv_file}")
    
    return training_dataframes

def prepare_training_data():
    print("Preparing training data...")

    print("Processing hourly data...")
    hourly_data = process_hourly_data()

    print("Processing weather data...")
    weather_data = process_weather_data()

    print("Combining data...")
    dataframes = combine_data(hourly_data, weather_data)

    print("Preprocessing done")
    return dataframes

if __name__ == "__main__":
    prepare_training_data()
