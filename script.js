function generateGraph() {
    const Li = document.getElementById('Li').value;
    const Ki = document.getElementById('Ki').value;
    const Aix = document.getElementById('Aix').value;
    const Aiy = document.getElementById('Aiy').value;
    const alpha_x = document.getElementById('x').value;
    const alpha_y = document.getElementById('y').value;

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
            alpha_y: alpha_y
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

        // Assuming utility is a single value, we'll plot it as a point on the graph
        const utilityTrace = {
            x: [data.utility],
            y: [data.utility],
            mode: 'markers',
            name: 'Utility',
            marker: {
                size: 10,
                color: 'red'
            }
        };

        const layout = {
            title: 'Production Possibilities Frontier (PPF) with Utility',
            xaxis: {
                title: 'Quantity of Good x'
            },
            yaxis: {
                title: 'Quantity of Good y'
            }
        };

        Plotly.newPlot('plot', [ppfTrace, utilityTrace], layout);
    })
    .catch(error => {
        console.error('Error fetching data:', error);
    });
}