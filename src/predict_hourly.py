import matplotlib.pyplot as plt
import pandas as pd
import datetime as dt
from train_model import load_model
from forecasts import get_forecast_for_date

MODELS = {"Paloheinä": load_model("Paloheinä"),
          "Pirkkola": load_model("Pirkkola"),
          "Hietaniemi": load_model("Hietaniemi")
          }

def predict(date=dt.datetime.now() + dt.timedelta(days=1), area="Paloheinä"):
    # Convert date str to datetime object
    if isinstance(date, str):
        date = dt.datetime.strptime(date, '%Y-%m-%d')
    # Load the model    
    # Get the precipitation data for the given date
    precipitation = get_forecast_for_date(date, area)
    # Check if an error occurred
    if type(precipitation) == str:
        return precipitation
    # Fill missing precipitation values with zeros
    forecast_hours = len(precipitation)
    if forecast_hours < 24:
        precipitation.extend([0] * (24 - forecast_hours))

    # Create a DataFrame with 24 rows, each representing an hour of the day
    week_of_year = date.isocalendar()[1]
    day_of_week = date.weekday()

    df = pd.DataFrame({
        'week_of_year': [week_of_year] * 24,
        'day_of_week': [day_of_week] * 24,
        'hour': range(24),
        'precipitation_mm': precipitation
    })

    # Predict the total minutes for each hour of the day
    df['total_minutes'] = MODELS[area].predict(df[['week_of_year', 'hour', 'day_of_week', 'precipitation_mm']])
    
    # Convert negative predictions to zero
    df['total_minutes'] = df['total_minutes'].clip(lower=0)

    return df, forecast_hours

def plot_predictions(df, date=dt.datetime.now() + dt.timedelta(days=1)):
    # Plot the predicted total minutes for each hour of the day
    plt.figure(figsize=(12, 6))
    plt.plot(df['hour'], df['total_minutes'], marker='o', label='Predicted Total Minutes', color='red')
    plt.plot(df['precipitation_mm']*10, marker='o', label='Precipitation (mm) * 10', color='blue')
    plt.xlabel('Hour of the Day')
    plt.ylabel('Total Minutes')
    plt.title(f'Predicted Total Minutes for {date.day}.{date.month}.{date.year}')
    plt.legend()
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    # forecast for tomorrow
    date = dt.datetime.now() + dt.timedelta(days=1)
    area = "Paloheinä"
    df = predict(date, area)
    plot_predictions(df, date)
