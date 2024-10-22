from flask import Flask
from flask_cors import CORS
from routes import initialize_routes

app = Flask(__name__)
CORS(app)
initialize_routes(app)
# Start app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
