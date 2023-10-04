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
    Li, Ki, Aix, Aiy, alpha_x, alpha_y = float(data['Li']), float(data['Ki']), float(data['Aix']), float(data['Aiy']), float(data['alpha_x']), float(data['alpha_y'])

    # Define the PPF function
    def ppf(qx):
        return Aiy * (Li - qx/Aix)**alpha_y * Ki**(1-alpha_y)

    # Utility function (simplified without beta_i)
    def utility(cx, cy):
        return cx + cy

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
    
    # Generate multiple indifference curves
    utilities = [0.25, 0.5, 0.75, 1.0, 1.25, 1.5]  # Example utility levels
    indifference_curves = []
    for u in utilities:
        cy_values = [u / qx if qx != 0 else 0 for qx in qx_values]
        indifference_curves.append({
            'utility': u,
            'qx': qx_values.tolist(),
            'qy': cy_values
        })

    return jsonify({
        'ppf': {
            'qx': qx_values.tolist(),
            'qy': ppf_values
        },
        'indifference_curves': indifference_curves
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))