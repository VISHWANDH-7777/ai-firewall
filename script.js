document.addEventListener('DOMContentLoaded', function () {
    // Initialize Chart.js
    const ctx = document.getElementById('trafficChart').getContext('2d');
    const trafficChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: [],
            datasets: [{
                label: 'Network Traffic (Packets/sec)',
                data: [],
                borderColor: '#38bdf8',
                backgroundColor: 'rgba(56, 189, 248, 0.1)',
                borderWidth: 2,
                fill: true,
                tension: 0.4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: true,
                    grid: {
                        color: 'rgba(255, 255, 255, 0.1)'
                    },
                    ticks: {
                        color: '#e2e8f0'
                    }
                },
                x: {
                    grid: {
                        color: 'rgba(255, 255, 255, 0.1)'
                    },
                    ticks: {
                        color: '#e2e8f0'
                    }
                }
            },
            plugins: {
                legend: {
                    labels: {
                        color: '#e2e8f0'
                    }
                }
            }
        }
    });

    // Update data function
    let packetCounts = [];
    let timeLabels = [];

    function updateChart() {
        if (packetCounts.length > 15) {
            packetCounts.shift();
            timeLabels.shift();
        }

        trafficChart.data.labels = timeLabels;
        trafficChart.data.datasets[0].data = packetCounts;
        trafficChart.update();
    }

    // Control buttons
    const startBtn = document.getElementById('startBtn');
    const stopBtn = document.getElementById('stopBtn');
    const launchAttackBtn = document.getElementById('launchAttackBtn');

    let updateInterval;

    startBtn.addEventListener('click', function () {
        fetch('/start_monitoring', { method: 'POST' })
            .then(response => response.json())
            .then(data => {
                console.log('Monitoring started:', data);
                startBtn.disabled = true;
                stopBtn.disabled = false;

                // Start updating data
                updateInterval = setInterval(fetchData, 2000);
            })
            .catch(error => console.error('Error:', error));
    });

    stopBtn.addEventListener('click', function () {
        fetch('/stop_monitoring', { method: 'POST' })
            .then(response => response.json())
            .then(data => {
                console.log('Monitoring stopped:', data);
                startBtn.disabled = false;
                stopBtn.disabled = true;

                // Stop updating data
                clearInterval(updateInterval);
            })
            .catch(error => console.error('Error:', error));
    });

    stopBtn.disabled = true;

    launchAttackBtn.addEventListener('click', function () {
        const attackType = document.getElementById('attackType').value;
        const targetIp = document.getElementById('targetIp').value;

        fetch('/launch_attack', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                attack_type: attackType,
                target: targetIp
            })
        })
            .then(response => response.json())
            .then(data => {
                console.log('Attack launched:', data);
                alert(`Attack launched: ${attackType} on ${targetIp}`);
            })
            .catch(error => console.error('Error:', error));
    });

    // Function to fetch and update data
    function fetchData() {
        fetch('/get_traffic_data')
            .then(response => response.json())
            .then(data => {
                // Update stats
                document.getElementById('totalPackets').textContent = data.stats.total_packets.toLocaleString();
                document.getElementById('threatsDetected').textContent = data.stats.threats_detected;
                document.getElementById('lastUpdated').textContent = data.stats.last_updated;

                // Update chart
                const currentTime = new Date().toLocaleTimeString();
                timeLabels.push(currentTime);
                packetCounts.push(data.traffic.length);
                updateChart();

                // Update threats list
                const threatsList = document.getElementById('threatsList');
                if (data.threats.length > 0) {
                    threatsList.innerHTML = '';
                    data.threats.slice().reverse().forEach(threat => {
                        const threatItem = document.createElement('div');
                        threatItem.className = 'threat-item';
                        threatItem.innerHTML = `
                            <div class="threat-info">
                                <div class="threat-type">${threat.type}</div>
                                <div class="threat-source">From: ${threat.source}</div>
                                <div class="threat-target">To: ${threat.target}</div>
                            </div>
                            <div class="threat-severity severity-${threat.severity.toLowerCase()}">${threat.severity}</div>
                            <div class="threat-time">${threat.timestamp}</div>
                        `;
                        threatsList.appendChild(threatItem);
                    });
                }

                // Update traffic table
                const trafficTableBody = document.getElementById('trafficTableBody');
                trafficTableBody.innerHTML = '';

                if (data.traffic.length > 0) {
                    data.traffic.slice().reverse().forEach(packet => {
                        const row = document.createElement('tr');
                        row.innerHTML = `
                            <td>${packet.timestamp}</td>
                            <td>${packet.source}</td>
                            <td>${packet.destination}</td>
                            <td>${packet.protocol}</td>
                            <td>${packet.size} bytes</td>
                            <td class="${packet.threat ? 'traffic-threat' : 'traffic-normal'}">
                                ${packet.threat ? 'THREAT' : 'Normal'}
                            </td>
                        `;
                        trafficTableBody.appendChild(row);
                    });
                }
            })
            .catch(error => console.error('Error fetching data:', error));
    }

    // Initial data fetch
    fetchData();
});
