from flask import Flask, jsonify, request
import numpy as np
from scipy.optimize import minimize

app = Flask(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.json
    # Extract data from the request
    Li, Ki, Aix, Aiy, x, y = data['Li'], data['Ki'], data['Aix'], data['Aiy'], data['x'], data['y']

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
