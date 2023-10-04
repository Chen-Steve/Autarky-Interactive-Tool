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
    def utility(cx, cy):
        return cx**beta_i * cy**(1-beta_i)

    # MRS function
    def mrs(cx, cy):
        mu_x = beta_i * cx**(beta_i - 1) * cy**(1-beta_i)
        mu_y = (1-beta_i) * cx**beta_i * cy**(-beta_i)
        return -mu_x/mu_y

    # Optimization problem to find the PPF
    def objective(q):
        qx, qy = q
        return -utility(qx, qy)

    constraints = (
        {'type': 'eq', 'fun': lambda q: q[0] - Aix * q[1]**alpha_x * Ki**(1-alpha_x)},
        {'type': 'ineq', 'fun': lambda q: Li - ((q[0]/(Aix * (q[0]/(Aix * Ki**(1-alpha_x)))**(alpha_x)))**(1/alpha_x) + ((q[1]/(Aiy * (q[1]/(Aiy * Ki**(1-alpha_y)))**(alpha_y)))**(1/alpha_y)))},
        {'type': 'ineq', 'fun': lambda q: Ki - ((q[0]/(Aix * (q[0]/(Aix * Li**alpha_x))**(1-alpha_x)))**(1/(1-alpha_x)) + (q[1]/(Aiy * (q[1]/(Aiy * Li**alpha_y))**(1-alpha_y)))**(1/(1-alpha_y)))},
        {'type': 'ineq', 'fun': lambda q: Li - q[1]},
        {'type': 'ineq', 'fun': lambda q: Ki - q[0]}
    )

    result = minimize(objective, [0.5, 0.5], constraints=constraints)

    # Find the tangency point
    qx_values = np.linspace(0, Aix*Li**alpha_x*Ki**(1-alpha_x), 100)
    ppf_values = [ppf(qxi) for qxi in qx_values]
    mrs_values = [mrs(qxi, qyi) for qxi, qyi in zip(qx_values, ppf_values)]

    # Assuming the PPF has a constant slope (MRT), find where MRS equals MRT
    mrt = (ppf_values[-1] - ppf_values[0]) / (qx_values[-1] - qx_values[0])
    tangency_index = np.argmin(np.abs(np.array(mrs_values) - mrt))
    tangency_qx = qx_values[tangency_index]
    tangency_qy = ppf_values[tangency_index]

    # Return the calculated data
    return jsonify({
        'qx': qx_values.tolist(),
        'qy': ppf_values,
        'tangency_qx': tangency_qx,
        'tangency_qy': tangency_qy
    })

if __name__ == '__main__':
    app.run(debug=True)
