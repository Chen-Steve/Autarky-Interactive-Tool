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
            x: data.ppf.qx,
            y: data.ppf.qy,
            mode: 'lines',
            name: 'PPF'
        };

        const traces = [ppfTrace];
        data.indifference_curves.forEach(curve => {
            traces.push({
                x: curve.qx,
                y: curve.qy,
                mode: 'lines',
                name: `U=${curve.utility}`
            });
        });

        const layout = {
            title: 'Production Possibilities Frontier (PPF) with Indifference Curves',
            xaxis: {
                title: 'Quantity of Good x'
            },
            yaxis: {
                title: 'Quantity of Good y'
            }
        };

        Plotly.newPlot('plot', traces, layout);
    })
    .catch(error => {
        console.error('Error fetching data:', error);
    });
}