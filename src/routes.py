from flask import request, jsonify
import predict_hourly as ph

# Route for predictions based on input data
def initialize_routes(app):
    @app.route('/predict', methods=['POST'])
    def predict_usage():
        data = request.json
        date = data.get('date')
        area = data.get('area')

        if not date or not area:
            return jsonify({'error': 'Please provide both date and area'}), 400
        
        df, forecast_hours = ph.predict(date, area)
        if forecast_hours < 24:
            df['precipitation_mm'][forecast_hours:] = "NaN"
        # return precipitation and usage minutes as list
        return jsonify(
            {
                'precipitation': df['precipitation_mm'].tolist(),
                'usage_minutes': df['total_minutes'].tolist(),
            }
        )