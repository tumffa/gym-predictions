# Gym Predictions

This project predicts usage for outdoor gyms in Helsinki and Espoo.

## Setup and usage

Using poetry, install dependencies and activate virtual environment
```bash
poetry install
```
```bash
poetry shell
```

Run the predictions with default parameters (tomorrow in Paloheinä)
```bash
python3 src/main.py
```

## Web App

To run the web app you need to have Node.js installed: https://nodejs.org/en/download/package-manager

Navigate to src/ui
```bash
cd src/ui
```

Install dependencies:
```bash
npm install
```

Run in dev mode:
```bash
npm run dev
```
