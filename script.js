function generateGraph() {
    const Li = document.getElementById('Li').value;
    const Ki = document.getElementById('Ki').value;
    const Aix = document.getElementById('Aix').value;
    const Aiy = document.getElementById('Aiy').value;
    const alpha_x = document.getElementById('x').value;
    const alpha_y = document.getElementById('y').value;
    const beta_i = document.getElementById('beta_i').value;  

    fetch('http://localhost:5000/calculate', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            Li: Li,
            Ki: Ki,
            Aix: Aix,
            Aiy: Aiy,
            alpha_x: alpha_x,
            alpha_y: alpha_y,
            beta_i: beta_i
        })
    })
    .then(response => response.json())
    .then(data => {
        const ppfTrace = {
            x: data.qx,
            y: data.qy,
            mode: 'lines',
            name: 'PPF'
        };

        // Plotting the tangent indifference curve as a point for simplicity
        const tangentTrace = {
            x: [data.tangency_qx],
            y: [data.tangency_qy],
            mode: 'markers',
            name: 'Tangent Point',
            marker: {
                size: 10,
                color: 'blue'
            }
        };

        const layout = {
            title: 'Production Possibilities Frontier (PPF) with Tangent Indifference Curve',
            xaxis: {
                title: 'Quantity of Good x'
            },
            yaxis: {
                title: 'Quantity of Good y'
            }
        };

        Plotly.newPlot('plot', [ppfTrace, tangentTrace], layout);
    })
    .catch(error => {
        console.error('Error fetching data:', error);
    });
}