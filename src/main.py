import preprocess
import predict_hourly
from flask import Flask
from flask_cors import CORS
from routes import initialize_routes

def main():
    app = Flask(__name__)
    CORS(app)
    initialize_routes(app)
    # Start app
    if __name__ == "__main__":
        app.run(debug=True)

if __name__ == "__main__":
    main()
