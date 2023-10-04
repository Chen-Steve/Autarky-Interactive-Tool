from flask import Flask, jsonify, request
import numpy as np
from scipy.optimize import minimize
from flask_cors import CORS


app = Flask(__name__)
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.json
    # Extract data from the request and convert to appropriate numeric types
    Li = float(data['Li'])
    Ki = float(data['Ki'])
    Aix = float(data['Aix'])
    Aiy = float(data['Aiy'])
    x = float(data['x'])
    y = float(data['y'])

    # Define the PPF function
    def ppf(qx):
        return Aiy * (Li - qx/Aix)**y * Ki**(1-y)

    # Return the calculated data
    return jsonify({
        'qx': np.linspace(0, Aix*Li**x*Ki**(1-x), 100).tolist(),
        'qy': [ppf(qxi) for qxi in np.linspace(0, Aix*Li**x*Ki**(1-x), 100)]
    })

if __name__ == '__main__':
    app.run(debug=True)
