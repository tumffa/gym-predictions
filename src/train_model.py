from sklearn.linear_model import Ridge
from sklearn.preprocessing import StandardScaler, PolynomialFeatures
from sklearn.pipeline import Pipeline
import pandas as pd


def train_model(area, degree=3):
    # Training data by gym area
    files = {
        "Paloheinä": "./processed_data/training_data_helsinkivantaa_weather.csv",
        "Pirkkola": "./processed_data/training_data_kumpula_weather.csv",
        "Hietaniemi": "./processed_data/training_data_kumpula_weather.csv"
    }
    df = pd.read_csv(files[area])

    # Filter the DataFrame by area
    df = df[df['area'] == area]

    # Convert localtime to datetime
    df['localtime'] = pd.to_datetime(df['localtime'])

    # Choose training columns
    train_columns = ['week_of_year', 'hour', 'day_of_week', 'precipitation_mm']

    # Prepare the features and target variable for training
    X_train_weather = df[train_columns]
    y_train_weather = df['total_minutes']

    # Create a polynomial regression model with Ridge regularization (degree=3 for cubic)
    polynomial_degree = degree
    model = Pipeline([
        ('poly_features', PolynomialFeatures(degree=polynomial_degree)),
        ('scaler', StandardScaler()),
        ('ridge_regression', Ridge(alpha=1.0))
    ])

    # Fit the model
    model.fit(X_train_weather, y_train_weather)

    return model
