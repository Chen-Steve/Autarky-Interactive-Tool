function generateGraph() {
    const Li = document.getElementById('Li').value;
    const Ki = document.getElementById('Ki').value;
    const Aix = document.getElementById('Aix').value;
    const Aiy = document.getElementById('Aiy').value;
    const x = document.getElementById('x').value;
    const y = document.getElementById('y').value;

    fetch('http://localhost:5000/calculate', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            Li, Ki, Aix, Aiy, x, y
        })
    })
    .then(response => response.json())
    .then(data => {
        const trace = {
            x: data.qx,
            y: data.qy,
            mode: 'lines'
        };
        Plotly.newPlot('plot', [trace]);
    });
}
