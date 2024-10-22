from flask import request, jsonify, send_from_directory
import predict_hourly as ph

# Route for predictions based on input data
def initialize_routes(app):
    @app.route('/')
    def serve_index():
        return send_from_directory(app.static_folder, 'index.html')
    
    @app.route('/<path:path>')
    def serve_static(path):
        return send_from_directory(app.static_folder, path)
    
    @app.route('/predict', methods=['POST'])
    def predict_usage():
        data = request.json
        date = data.get('date')
        area = data.get('area')

        if not date or not area:
            return jsonify({'error': 'Please provide both date and area'}), 400
        
        df = ph.predict(date, area)
        # return precipitation and usage minutes as list
        return jsonify(
            {
                'precipitation': df['precipitation_mm'].tolist(),
                'usage_minutes': df['total_minutes'].tolist(),
            }
        )