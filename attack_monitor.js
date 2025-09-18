// Initialize Chart.js for impact visualization
const ctx = document.getElementById('impactChart').getContext('2d');
const impactChart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: [],
        datasets: [
            {
                label: 'Server Load',
                data: [],
                borderColor: '#ef4444',
                backgroundColor: 'rgba(239, 68, 68, 0.1)',
                borderWidth: 2,
                fill: true
            },
            {
                label: 'Response Time (ms/10)',
                data: [],
                borderColor: '#3b82f6',
                backgroundColor: 'rgba(59, 130, 246, 0.1)',
                borderWidth: 2,
                fill: true
            },
            {
                label: 'AI Confidence',
                data: [],
                borderColor: '#10b981',
                backgroundColor: 'rgba(16, 185, 129, 0.1)',
                borderWidth: 2,
                fill: true
            }
        ]
    },
    options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
            y: {
                beginAtZero: true,
                max: 100,
                grid: { color: 'rgba(255, 255, 255, 0.1)' },
                ticks: { color: '#e2e8f0' }
            },
            x: {
                grid: { color: 'rgba(255, 255, 255, 0.1)' },
                ticks: { color: '#e2e8f0' }
            }
        },
        plugins: {
            legend: {
                labels: { color: '#e2e8f0' }
            }
        }
    }
});

// Data arrays for chart
const timeLabels = [];
const serverLoadData = [];
const responseTimeData = [];
const aiConfidenceData = [];

// Update chart function
function updateChart() {
    if (timeLabels.length > 15) {
        timeLabels.shift();
        serverLoadData.shift();
        responseTimeData.shift();
        aiConfidenceData.shift();
    }

    impactChart.data.labels = timeLabels;
    impactChart.data.datasets[0].data = serverLoadData;
    impactChart.data.datasets[1].data = responseTimeData;
    impactChart.data.datasets[2].data = aiConfidenceData;
    impactChart.update();
}

// Add log entry
function addLogEntry(message, type = 'info') {
    const logContainer = document.getElementById('attackLog');
    const logEntry = document.createElement('div');
    logEntry.className = `log-entry ${type}`;

    const now = new Date();
    const timestamp = now.toLocaleTimeString();

    logEntry.innerHTML = `
        <div class="log-time">${timestamp}</div>
        <div class="log-message">${message}</div>
    `;

    logContainer.appendChild(logEntry);
    logContainer.scrollTop = logContainer.scrollHeight;
}

// Launch attack function
function launchAttack(attackType) {
    fetch('/launch_attack', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            attack_type: attackType,
            target: '192.168.1.1'
        })
    })
        .then(response => response.json())
        .then(data => {
            addLogEntry(`🚀 ${attackType.toUpperCase()} attack launched against 192.168.1.1`, 'threat');
            console.log('Attack launched:', data);
        })
        .catch(error => {
            addLogEntry('❌ Failed to launch attack', 'threat');
            console.error('Error:', error);
        });
}

// Trigger AI mitigation
function triggerAIMitigation() {
    fetch('/trigger_ai_mitigation', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' }
    })
        .then(response => response.json())
        .then(data => {
            addLogEntry('🛡️ AI mitigation triggered manually', 'mitigation');
            console.log('AI mitigation triggered:', data);
        })
        .catch(error => {
            addLogEntry('❌ Failed to trigger AI mitigation', 'mitigation');
            console.error('Error:', error);
        });
}

// Update system health display
function updateSystemHealth(health) {
    if (!health) return;

    // Update metrics
    document.getElementById('serverLoad').textContent = `${Math.round(health.server_load * 100)}%`;
    document.getElementById('responseTime').textContent = `${Math.round(health.response_time)}ms`;
    document.getElementById('healthScore').textContent = `${Math.round(health.health_score)}%`;

    // Update progress bars
    document.getElementById('serverLoadBar').style.width = `${health.server_load * 100}%`;
    document.getElementById('responseTimeBar').style.width = `${Math.min(100, health.response_time / 20)}%`;
    document.getElementById('healthScoreBar').style.width = `${health.health_score}%`;

    // Update status
    const statusElement = document.getElementById('systemStatus');
    statusElement.textContent = health.status.toUpperCase();
    statusElement.className = `status-${health.status}`;

    // Update chart data
    const now = new Date();
    timeLabels.push(now.toLocaleTimeString());
    serverLoadData.push(health.server_load * 100);
    responseTimeData.push(health.response_time / 10); // Scale for chart
    updateChart();
}

// Update AI status
function updateAIStatus(aiStatus) {
    if (!aiStatus) return;

    document.getElementById('detectionConfidence').textContent = `${Math.round(aiStatus.detection_confidence * 100)}%`;
    document.getElementById('mitigationProgress').textContent = `${Math.round(aiStatus.mitigation_progress * 100)}%`;
    document.getElementById('threatsDetected').textContent = aiStatus.threats_detected;
    document.getElementById('attacksBlocked').textContent = aiStatus.attacks_blocked;

    // Update AI bars
    document.getElementById('detectionBar').style.width = `${aiStatus.detection_confidence * 100}%`;
    document.getElementById('mitigationBar').style.width = `${aiStatus.mitigation_progress * 100}%`;

    // Update chart
    aiConfidenceData.push(aiStatus.detection_confidence * 100);
    updateChart();
}

// Fetch real-time data
function fetchRealTimeData() {
    fetch('/get_realtime_data')
        .then(response => response.json())
        .then(data => {
            updateSystemHealth(data.system_health);
            updateAIStatus(data.ai_status);

            // Add new log entries
            if (data.recent_events && data.recent_events.length > 0) {
                data.recent_events.forEach(event => {
                    if (!document.querySelector(`[data-event-id="${event.id}"]`)) {
                        addLogEntry(event.message, event.type);
                    }
                });
            }
        })
        .catch(error => console.error('Error fetching real-time data:', error));
}

// Start real-time monitoring
let monitorInterval;
function startMonitoring() {
    monitorInterval = setInterval(fetchRealTimeData, 1000); // Update every second
    addLogEntry('✅ Real-time monitoring started', 'info');
}

// Stop monitoring
function stopMonitoring() {
    if (monitorInterval) {
        clearInterval(monitorInterval);
        addLogEntry('⏹️ Real-time monitoring stopped', 'info');
    }
}

// Initialize when page loads
document.addEventListener('DOMContentLoaded', function () {
    startMonitoring();

    // Add initial chart data
    for (let i = 0; i < 10; i++) {
        timeLabels.push('');
        serverLoadData.push(30);
        responseTimeData.push(12);
        aiConfidenceData.push(0);
    }
    updateChart();
});

// Clean up when leaving page
window.addEventListener('beforeunload', stopMonitoring);