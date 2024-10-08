import preprocess
import predict_hourly

def main():
    preprocess.prepare_training_data()
    df = predict_hourly.predict()
    predict_hourly.plot_predictions(df)

if __name__ == "__main__":
    main()
