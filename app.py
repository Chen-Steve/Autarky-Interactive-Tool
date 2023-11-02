from flask import Flask, jsonify, request, render_template
import numpy as np
from scipy.optimize import fsolve
from flask_cors import CORS
import os

app = Flask(__name__, static_folder="static", template_folder="templates")
CORS(app)

# Define the production functions outside of the route handler
def production_x(L_x, K_x, A_x, alpha_x):
    return A_x * L_x**alpha_x * K_x**(1-alpha_x)

def production_y(L_y, K_y, A_y, alpha_y):
    return A_y * L_y**alpha_y * K_y**(1-alpha_y)

# Define the utility function
def utility(cx, cy, beta):
    return cx**beta * cy**(1 - beta)

# Define the MRT function
def MRT(L_x, K_x, L_y, K_y, A_x, alpha_x, A_y, alpha_y):
    MP_L_x = alpha_x * (K_x/L_x)**(1-alpha_x)
    MP_L_y = alpha_y * (K_y/L_y)**(1-alpha_y)
    return -MP_L_x / MP_L_y

# Define the MRS function
def MRS(q_x, q_y, beta):
    return (beta / (1 - beta)) * (q_y / q_x)

def solve_for_cy(cx, u, beta):
    return (u / (cx**beta))**(1/(1 - beta))

# Define a function to find the tangency point
def tangency_point(L, K, A_x, alpha_x, A_y, alpha_y, beta):
    # Initial guess for L_x and K_x
    guess = [L/2, K/2]
    
    # Define the equations to solve
    def equations(p):
        L_x, K_x = p
        L_y = L - L_x
        K_y = K - K_x
        q_x = production_x(L_x, K_x, A_x, alpha_x)
        q_y = production_y(L_y, K_y, A_y, alpha_y)
        return (MRT(L_x, K_x, L_y, K_y, A_x, alpha_x, A_y, alpha_y) - MRS(q_x, q_y, beta), L_x + L_y - L)
    
    # Solve for L_x and K_x
    L_x, K_x = fsolve(equations, guess)
    # Calculate q_x and q_y
    q_x = production_x(L_x, K_x, A_x, alpha_x)
    q_y = production_y(L - L_x, K - K_x, A_y, alpha_y)
    
    return q_x, q_y

@app.route('/')
def index():
    return render_template('graph.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.json

    # Extract data from the request
    Li, Ki, Aix, Aiy, alpha_x, alpha_y, beta = (float(data['Li']), float(data['Ki']), float(data['Aix']), 
                                                 float(data['Aiy']), float(data['alpha_x']), float(data['alpha_y']), 
                                                 float(data['beta']))

    # Find the tangency point
    q_x_tangent, q_y_tangent = tangency_point(Li, Ki, Aix, alpha_x, Aiy, alpha_y, beta)

    # Generate PPF values
    qx_values = np.linspace(0, q_x_tangent, 100)
    ppf_values = [production_y(Li - qx/Aix, Ki - qx*(1-alpha_x)/Aix, Aiy, alpha_y) for qx in qx_values]

    # Generate multiple indifference curves
    utilities = [utility(q_x_tangent, q_y_tangent, beta) * u for u in [0.8, 1, 1.2]]  # Example utility levels
    indifference_curves = []
    for u in utilities:
        cy_values = [(u / (qx**beta))**(1/(1 - beta)) if qx != 0 else 0 for qx in qx_values]
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
        'indifference_curves': indifference_curves,
        'tangency_point': {'qx': q_x_tangent, 'qy': q_y_tangent}
    })

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)