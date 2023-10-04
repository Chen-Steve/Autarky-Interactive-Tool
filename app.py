from flask import Flask, jsonify, request
import numpy as np
from scipy.optimize import minimize
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.json

    # Extract data from the request
    Li, Ki, Aix, Aiy, alpha_x, alpha_y, beta_i = float(data['Li']), float(data['Ki']), float(data['Aix']), float(data['Aiy']), float(data['alpha_x']), float(data['alpha_y']), float(data['beta_i'])

    # Define the PPF function
    def ppf(qx):
        return Aiy * (Li - qx/Aix)**alpha_y * Ki**(1-alpha_y)

    # Utility function
    def utility(cy):
        return cy**beta_i * cy**(1-beta_i)

    # Optimization problem to find the PPF
    def objective(q):
        qx, qy = q
        return -utility(qy)

    constraints = (
        {'type': 'eq', 'fun': lambda q: q[0] - Aix * q[1]**alpha_x * Ki**(1-alpha_x)},
        {'type': 'ineq', 'fun': lambda q: Li - q[1]},
        {'type': 'ineq', 'fun': lambda q: Ki - q[0]}
    )

    result = minimize(objective, [0.5, 0.5], constraints=constraints)

    # Return the calculated data
    return jsonify({
        'qx': np.linspace(0, Aix*Li**alpha_x*Ki**(1-alpha_x), 100).tolist(),
        'qy': [ppf(qxi) for qxi in np.linspace(0, Aix*Li**alpha_x*Ki**(1-alpha_x), 100)],
        'utility': utility(result.x[1])
    })

if __name__ == '__main__':
    app.run(debug=True)