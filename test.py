import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize
from ipywidgets import interact, FloatSlider
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.graph_objs as go

# Initialize the Dash app
app = dash.Dash(__name__)

# Define the app layout
app.layout = html.Div([
    html.H1("PPF and Indifference Curves"),
    
     # Sliders for parameters
    html.Label('L_bar'),
    dcc.Slider(id='L_bar-slider', min=50, max=150, value=100, step=5, marks={i: str(i) for i in range(50, 151, 5)}),
    
    html.Label('K_bar'),
    dcc.Slider(id='K_bar-slider', min=50, max=150, value=100, step=5, marks={i: str(i) for i in range(50, 151, 5)}),
    
    html.Label('A_x'),
    dcc.Slider(id='A_x-slider', min=0.5, max=2, value=1, step=0.1, marks={i: str(i) for i in np.arange(0.5, 2.1, 0.1)}),
    
    html.Label('alpha_x'),
    dcc.Slider(id='alpha_x-slider', min=0.1, max=0.9, value=0.5, step=0.1, marks={i: str(i) for i in np.arange(0.1, 1, 0.1)}),
    
    html.Label('A_y'),
    dcc.Slider(id='A_y-slider', min=0.5, max=2, value=1, step=0.1, marks={i: str(i) for i in np.arange(0.5, 2.1, 0.1)}),
    
    html.Label('alpha_y'),
    dcc.Slider(id='alpha_y-slider', min=0.1, max=0.9, value=0.5, step=0.1, marks={i: str(i) for i in np.arange(0.1, 1, 0.1)}),
    
    html.Label('beta'),
    dcc.Slider(id='beta-slider', min=0.1, max=0.9, value=0.5, step=0.1, marks={i: str(i) for i in np.arange(0.1, 1, 0.1)}),

    # Graph to display PPF and indifference curves
    dcc.Graph(id='graph')
])

def PPF(q_x, L_bar, K_bar, A_x, alpha_x, A_y, alpha_y):
    # Calculate L_x and K_x from q_x
    L_x = (q_x / (A_x * K_bar**(1-alpha_x)))**(1/alpha_x)
    K_x = q_x / (A_x * L_x**alpha_x)
    
    # Remaining labor and capital for q_y
    L_y = L_bar - L_x
    K_y = K_bar - K_x
    
    # If the constraints are violated, return a NaN (Not a Number) for that q_x
    if (L_x + L_y > L_bar).any() or (K_x + K_y > K_bar).any():
        return np.nan
    
    # Calculate q_y given L_y and K_y
    q_y = A_y * L_y**alpha_y * K_y**(1-alpha_y)
    
    return q_y

def indifference_curve(U, q_x, beta):
    # Given utility U and q_x, calculate q_y
    return (U / q_x**beta)**(1/(1-beta))

def plot_graphs_with_multiple_indifference_curves(L_bar=100, K_bar=100, A_x=1, alpha_x=0.5, A_y=1, alpha_y=0.5, beta=0.5):
    q_x_values = np.linspace(0.1, 50, 100)
    ppf_values = PPF(q_x_values, L_bar, K_bar, A_x, alpha_x, A_y, alpha_y)
    
    # Plot PPF
    plt.figure(figsize=(10, 6))
    plt.plot(q_x_values, ppf_values, label='PPF', linewidth=2)
    
    # Plot multiple indifference curves
    for U in [5, 10, 15, 20, 25]:
        indifference_values = indifference_curve(U, q_x_values, beta)
        plt.plot(q_x_values, indifference_values, label=f'U={U}')
    
    tangency_x, tangency_y = find_tangency(q_x_values, ppf_values, indifference_curve(10, q_x_values, beta))
    plt.scatter(tangency_x, tangency_y, color='red', label='Tangency Point')


def find_tangency(q_x_values, ppf_values, indifference_values):
    # Calculate the differences between PPF and indifference curve values
    differences = ppf_values - indifference_values
    
    # Find the index where the difference is closest to zero
    idx = np.argmin(np.abs(differences))
    
    return q_x_values[idx], ppf_values[idx]

# Using the previous plotting function
def plot_graphs_with_tangency(L_bar=100, K_bar=100, A_x=1, alpha_x=0.5, A_y=1, alpha_y=0.5, beta=0.5):
    q_x_values = np.linspace(0.1, 50, 100)
    ppf_values = PPF(q_x_values, L_bar, K_bar, A_x, alpha_x, A_y, alpha_y)
    indifference_values = indifference_curve(10, q_x_values, beta)
    
    tangency_x, tangency_y = find_tangency(q_x_values, ppf_values, indifference_values)
    
    plt.figure(figsize=(10, 6))
    plt.plot(q_x_values, ppf_values, label='PPF')
    plt.plot(q_x_values, indifference_values, label='Indifference Curve')
    plt.scatter(tangency_x, tangency_y, color='red', label='Tangency Point')
    plt.xlabel('q_x')
    plt.ylabel('q_y')
    plt.legend()
    plt.grid(True)
    plt.title('PPF, Multiple Indifference Curve, and Tangency Point')
    plt.show()

# define callback to include all slider inputs
@app.callback(
    Output('graph', 'figure'),
    [Input('L_bar-slider', 'value'),
     Input('K_bar-slider', 'value'),
     Input('A_x-slider', 'value'),
     Input('alpha_x-slider', 'value'),
     Input('A_y-slider', 'value'),
     Input('alpha_y-slider', 'value'),
     Input('beta-slider', 'value')]
)
def update_graph(L_bar, K_bar, A_x, alpha_x, A_y, alpha_y, beta):
    q_x_values = np.linspace(0.1, 50, 100)
    ppf_values = PPF(q_x_values, L_bar, K_bar, A_x, alpha_x, A_y, alpha_y)
    indifference_values = indifference_curve(10, q_x_values, beta)
    
    return {
        'data': [
            go.Scatter(x=q_x_values, y=ppf_values, mode='lines', name='PPF'),
            go.Scatter(x=q_x_values, y=indifference_values, mode='lines', name='Indifference Curve')
        ],
        'layout': go.Layout(title='PPF and Indifference Curve', xaxis=dict(title='q_x'), yaxis=dict(title='q_y'))
    }

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)