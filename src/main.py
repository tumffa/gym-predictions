from flask import Flask
from flask_cors import CORS
from routes import initialize_routes

def main():
    app = Flask(__name__, static_folder='ui/build')
    CORS(app)
    initialize_routes(app)
    # Start app
    if __name__ == "__main__":
        app.run(host="0.0.0.0", port=8080)

if __name__ == "__main__":
    main()
