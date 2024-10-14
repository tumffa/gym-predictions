from flask import request, jsonify
from predict_hourly import predict

# Route for predictions based on input data
def initialize_routes(app):
    @app.route('/predict', methods=['POST'])
    def predict_usage():
        data = request.json
        date = data.get('date')
        area = data.get('area')

        if not date or not area:
            return jsonify({'error': 'Please provide both date and area'}), 400
        
        df = predict(date, area)
        # return precipitation and usage minutes as list
        return jsonify(
            {
                'precipitation': df['precipitation_mm'].tolist(),
                'usage_minutes': df['total_minutes'].tolist()
            }
        )