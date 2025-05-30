
// let cachedNetworkData = null;
// let cachedSystemData = null;
// let isDarkMode = false;

// async function fetchNetworkStatus() {
//     const statusDiv = document.getElementById("networkStatus");

//     if (cachedNetworkData) {
//         updateNetworkStatusUI(cachedNetworkData);
//     } else {
//         statusDiv.innerHTML = "📡 Fetching data...";
//     }

//     try {
//         const response = await fetch("http://127.0.0.1:8000/network-status");
//         const data = await response.json();

//         console.log("Data fetched:", data);

//         if (data.status === "success") {
//             cachedNetworkData = data.data;
//             updateNetworkStatusUI(cachedNetworkData);
//         } else {
//             statusDiv.innerHTML = `<span style="color: red;">⚠️ ${data.message}</span>`;
//         }
//     } catch (error) {
//         console.error("Error fetching network status:", error);
//         statusDiv.innerHTML = "<span style='color: red;'>⚠️ Failed to fetch data.</span>";
//     }
// }

// async function fetchSystemMetrics() {
//     const systemDiv = document.getElementById("systemMetrics");

//     if (cachedSystemData) {
//         updateSystemMetricsUI(cachedSystemData);
//     } else {
//         systemDiv.innerHTML = "🖥️ Fetching data...";
//     }

//     try {
//         const response = await fetch("http://127.0.0.1:8000/system-metrics");
//         const data = await response.json();

//         if (data.status === "success") {
//             cachedSystemData = data.data;
//             updateSystemMetricsUI(cachedSystemData);
//         } else {
//             systemDiv.innerHTML = `<span style="color: red;">⚠️ ${data.message}</span>`;
//         }
//     } catch (error) {
//         console.error("Error fetching system metrics:", error);
//         systemDiv.innerHTML = `<span style="color: red;">⚠️ Failed to fetch system metrics: ${error.message}</span>`;
//     }
// }

// async function fetchNetworkStatusPDF() {
//     const statusDiv = document.getElementById("networkStatus");
//     statusDiv.innerHTML = "📊 Generating Network Status PDF...";

//     try {
//         const response = await fetch("http://127.0.0.1:8000/network-status-pdf");
//         if (response.ok) {
//             const blob = await response.blob();
//             const url = window.URL.createObjectURL(blob);
//             const a = document.createElement('a');
//             a.href = url;
//             a.download = 'network_status_report.pdf';
//             document.body.appendChild(a);
//             a.click();
//             a.remove();
//             statusDiv.innerHTML = "📥 Network Status PDF downloaded successfully!";
//             alert("Network Status PDF generated and downloaded successfully!");
//         } else {
//             const data = await response.json();
//             statusDiv.innerHTML = `<span style="color: red;">⚠️ ${data.message}</span>`;
//         }
//     } catch (error) {
//         console.error("Error fetching network status PDF:", error);
//         statusDiv.innerHTML = "<span style='color: red;'>⚠️ Failed to fetch network status PDF.</span>";
//     }
// }

// async function fetchReport() {
//     const reportDiv = document.getElementById("networkReport");
//     reportDiv.innerHTML = "📊 Generating Operations Report PDF...";

//     try {
//         // Fetch network metrics first to display
//         const networkResponse = await fetch("http://127.0.0.1:8000/network-status");
//         const networkData = await networkResponse.json();
//         if (networkData.status === "success") {
//             cachedNetworkData = networkData.data;
//             updateNetworkStatusUI(cachedNetworkData); // Display metrics immediately
//         }

//         // Generate and download the PDF
//         const response = await fetch("http://127.0.0.1:8000/generate-report");
//         if (response.ok) {
//             const blob = await response.blob();
//             const url = window.URL.createObjectURL(blob);
//             const a = document.createElement('a');
//             a.href = url;
//             a.download = 'network_operations_report.pdf';
//             document.body.appendChild(a);
//             a.click();
//             a.remove();
//             reportDiv.innerHTML = `<div>${JSON.stringify(cachedNetworkData, null, 2)}</div>`; // Display metrics after download
//             alert("Operations Report PDF generated and downloaded successfully!");
//         } else {
//             const data = await response.json();
//             reportDiv.innerHTML = `<span style="color: red;">⚠️ ${data.message}</span>`;
//         }
//     } catch (error) {
//         console.error("Error fetching operations report PDF:", error);
//         reportDiv.innerHTML = "<span style='color: red;'>⚠️ Failed to fetch operations report PDF.</span>";
//     }
// }

// async function fetchSystemMetricsPDF() {
//     const systemDiv = document.getElementById("systemMetrics");
//     systemDiv.innerHTML = "🖥️ Generating System Metrics PDF...";

//     try {
//         const response = await fetch("http://127.0.0.1:8000/system-metrics-pdf");
//         if (response.ok) {
//             const blob = await response.blob();
//             const url = window.URL.createObjectURL(blob);
//             const a = document.createElement('a');
//             a.href = url;
//             a.download = 'system_metrics_report.pdf';
//             document.body.appendChild(a);
//             a.click();
//             a.remove();
//             systemDiv.innerHTML = "📥 System Metrics PDF downloaded successfully!";
//             alert("System Metrics PDF generated and downloaded successfully!");
//         } else {
//             const data = await response.json();
//             systemDiv.innerHTML = `<span style="color: red;">⚠️ ${data.message}</span>`;
//         }
//     } catch (error) {
//         console.error("Error fetching system metrics PDF:", error);
//         systemDiv.innerHTML = "<span style='color: red;'>⚠️ Failed to fetch system metrics PDF.</span>";
//     }
// }

// function updateNetworkStatusUI(metrics) {
//     const statusDiv = document.getElementById("networkStatus");
//     let metricsHtml = "<ul>";
//     metrics.forEach(metric => {
//         metricsHtml += `<li>${metric.name}: ${metric.lastvalue}</li>`;
//     });
//     metricsHtml += "</ul>";
//     statusDiv.innerHTML = metricsHtml;
// }

// function updateSystemMetricsUI(metrics) {
//     const systemDiv = document.getElementById("systemMetrics");
//     let metricsHtml = "<div>";
//     for (let [category, data] of Object.entries(metrics)) {
//         metricsHtml += `<h3>${category}</h3><ul>`;
//         for (let [name, value] of Object.entries(data)) {
//             if (Array.isArray(value)) {
//                 value.forEach(item => metricsHtml += `<li>${name}: ${item}</li>`);
//             } else if (typeof value === 'object' && value !== null) {
//                 for (let [subName, subValue] of Object.entries(value)) {
//                     metricsHtml += `<li>${name}: ${subName} - ${subValue}</li>`;
//                 }
//             } else {
//                 metricsHtml += `<li>${name}: ${value}</li>`;
//             }
//         }
//         metricsHtml += "</ul>";
//     }
//     metricsHtml += "</div>";
//     systemDiv.innerHTML = metricsHtml;
// }

// // Auto-refresh data every 10 seconds
// setInterval(() => {
//     fetchNetworkStatus();
//     fetchSystemMetrics();
// }, 10000);
// fetchNetworkStatus();
// fetchSystemMetrics();

// // Dark mode toggle
// document.getElementById('mode-toggle').addEventListener('click', () => {
//     isDarkMode = !isDarkMode;
//     document.body.classList.toggle('dark-mode', isDarkMode);
//     document.getElementById('mode-toggle').textContent = isDarkMode ? 'Toggle Light Mode' : 'Toggle Dark Mode';
// });

let cachedNetworkData = null;
let cachedSystemData = null;
let isDarkMode = false;

async function fetchNetworkStatus() {
    const statusDiv = document.getElementById("networkStatus");

    if (cachedNetworkData) {
        updateNetworkStatusUI(cachedNetworkData);
    } else {
        statusDiv.innerHTML = "📡 Fetching data...";
    }

    try {
        const response = await fetch("http://127.0.0.1:8000/network-status");
        const data = await response.json();

        console.log("Data fetched:", data);

        if (data.status === "success") {
            cachedNetworkData = data.data;
            updateNetworkStatusUI(cachedNetworkData);
        } else {
            statusDiv.innerHTML = `<span style="color: red;">⚠️ ${data.message}</span>`;
        }
    } catch (error) {
        console.error("Error fetching network status:", error);
        statusDiv.innerHTML = "<span style='color: red;'>⚠️ Failed to fetch data.</span>";
    }
}

async function fetchSystemMetrics() {
    const systemDiv = document.getElementById("systemMetrics");

    if (cachedSystemData) {
        updateSystemMetricsUI(cachedSystemData);
    } else {
        systemDiv.innerHTML = "🖥️ Fetching data...";
    }

    try {
        const response = await fetch("http://127.0.0.1:8000/system-metrics");
        const data = await response.json();

        if (data.status === "success") {
            cachedSystemData = data.data;
            updateSystemMetricsUI(cachedSystemData);
        } else {
            systemDiv.innerHTML = `<span style="color: red;">⚠️ ${data.message}</span>`;
        }
    } catch (error) {
        console.error("Error fetching system metrics:", error);
        systemDiv.innerHTML = `<span style="color: red;">⚠️ Failed to fetch system metrics: ${error.message}</span>`;
    }
}

async function fetchNetworkStatusPDF() {
    const statusDiv = document.getElementById("networkStatus");
    statusDiv.innerHTML = "📊 Generating Network Status PDF...";

    try {
        const response = await fetch("http://127.0.0.1:8000/network-status-pdf");
        if (response.ok) {
            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'network_status_report.pdf';
            document.body.appendChild(a);
            a.click();
            a.remove();
            statusDiv.innerHTML = "📥 Network Status PDF downloaded successfully!";
            alert("Network Status PDF generated and downloaded successfully!");
        } else {
            const data = await response.json();
            statusDiv.innerHTML = `<span style="color: red;">⚠️ ${data.message}</span>`;
        }
    } catch (error) {
        console.error("Error fetching network status PDF:", error);
        statusDiv.innerHTML = "<span style='color: red;'>⚠️ Failed to fetch network status PDF.</span>";
    }
}

async function fetchReport() {
    const reportDiv = document.getElementById("networkReport");
    reportDiv.innerHTML = "📊 Generating Operations Report PDF...";

    try {
        // Fetch network metrics first to display
        const networkResponse = await fetch("http://127.0.0.1:8000/network-status");
        const networkData = await networkResponse.json();
        if (networkData.status === "success") {
            cachedNetworkData = networkData.data;
            updateNetworkStatusUI(cachedNetworkData); // Display metrics immediately
        }

        // Generate and download the PDF
        const response = await fetch("http://127.0.0.1:8000/generate-report");
        if (response.ok) {
            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'network_operations_report.pdf';
            document.body.appendChild(a);
            a.click();
            a.remove();
            reportDiv.innerHTML = `<div>${JSON.stringify(cachedNetworkData, null, 2)}</div>`; // Display metrics after download
            alert("Operations Report PDF generated and downloaded successfully!");
        } else {
            const data = await response.json();
            reportDiv.innerHTML = `<span style="color: red;">⚠️ ${data.message}</span>`;
        }
    } catch (error) {
        console.error("Error fetching operations report PDF:", error);
        reportDiv.innerHTML = "<span style='color: red;'>⚠️ Failed to fetch operations report PDF.</span>";
    }
}

async function fetchSystemMetricsPDF() {
    const systemDiv = document.getElementById("systemMetrics");
    systemDiv.innerHTML = "🖥️ Generating System Metrics PDF...";

    try {
        const response = await fetch("http://127.0.0.1:8000/system-metrics-pdf");
        if (response.ok) {
            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'system_metrics_report.pdf';
            document.body.appendChild(a);
            a.click();
            a.remove();
            systemDiv.innerHTML = "📥 System Metrics PDF downloaded successfully!";
            alert("System Metrics PDF generated and downloaded successfully!");
        } else {
            const data = await response.json();
            systemDiv.innerHTML = `<span style="color: red;">⚠️ ${data.message}</span>`;
        }
    } catch (error) {
        console.error("Error fetching system metrics PDF:", error);
        systemDiv.innerHTML = "<span style='color: red;'>⚠️ Failed to fetch system metrics PDF.</span>";
    }
}

function updateNetworkStatusUI(metrics) {
    const statusDiv = document.getElementById("networkStatus");
    let metricsHtml = "<ul>";
    metrics.forEach(metric => {
        metricsHtml += `<li>${metric.name}: ${metric.lastvalue}</li>`;
    });
    metricsHtml += "</ul>";
    statusDiv.innerHTML = metricsHtml;
}

function updateSystemMetricsUI(metrics) {
    const systemDiv = document.getElementById("systemMetrics");
    let metricsHtml = "<div>";
    for (let [category, data] of Object.entries(metrics)) {
        metricsHtml += `<h3>${category}</h3><ul>`;
        for (let [name, value] of Object.entries(data)) {
            if (Array.isArray(value)) {
                value.forEach(item => metricsHtml += `<li>${name}: ${item}</li>`);
            } else if (typeof value === 'object' && value !== null) {
                for (let [subName, subValue] of Object.entries(value)) {
                    metricsHtml += `<li>${name}: ${subName} - ${subValue}</li>`;
                }
            } else {
                metricsHtml += `<li>${name}: ${value}</li>`;
            }
        }
        metricsHtml += "</ul>";
    }
    metricsHtml += "</div>";
    systemDiv.innerHTML = metricsHtml;
}

// Auto-refresh data every 10 seconds
setInterval(() => {
    fetchNetworkStatus();
    fetchSystemMetrics();
}, 10000);
fetchNetworkStatus();
fetchSystemMetrics();

// Dark mode toggle
document.getElementById('mode-toggle').addEventListener('click', () => {
    isDarkMode = !isDarkMode;
    document.body.classList.toggle('dark-mode', isDarkMode);
    document.getElementById('mode-toggle').textContent = isDarkMode ? 'Toggle Light Mode' : 'Toggle Dark Mode';
});