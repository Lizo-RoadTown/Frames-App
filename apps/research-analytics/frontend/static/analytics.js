/**
 * FRAMES Analytics Dashboard
 * Dynamic data visualization and exploration
 */

let chart = null;
let availableMetrics = [];
let availableDimensions = [];
let universities = [];
let projects = [];
let teams = [];

// Initialize on page load
window.addEventListener('DOMContentLoaded', async () => {
    await loadDimensionsAndMetrics();
    await loadFilterOptions();
    setupEventListeners();

    // Set default selection if university is in URL
    const urlParams = new URLSearchParams(window.location.search);
    const universityId = urlParams.get('university');
    if (universityId) {
        document.getElementById('filterUniversity').value = universityId;
        document.getElementById('universityName').textContent = `${universityId} Analytics`;
    }
});

// Load available metrics and dimensions from API
async function loadDimensionsAndMetrics() {
    try {
        const response = await fetch(`${API_BASE_URL}/analytics/dimensions`);
        const data = await response.json();

        availableMetrics = data.metrics;
        availableDimensions = data.dimensions;

        populateMetricSelect();
    } catch (error) {
        console.error('Error loading dimensions:', error);
        showError('Failed to load analytics configuration');
    }
}

// Populate metric dropdown
function populateMetricSelect() {
    const metricSelect = document.getElementById('metricSelect');

    availableMetrics.forEach(metric => {
        const option = document.createElement('option');
        option.value = metric.value;
        option.textContent = metric.label;
        option.dataset.description = metric.description;
        metricSelect.appendChild(option);
    });
}

// Update groupBy options based on selected metric
function updateGroupByOptions() {
    const metricSelect = document.getElementById('metricSelect');
    const groupBySelect = document.getElementById('groupBySelect');
    const metricHint = document.getElementById('metricHint');

    const selectedMetric = metricSelect.value;

    // Clear existing options
    groupBySelect.innerHTML = '<option value="">No grouping (total only)</option>';

    if (!selectedMetric) {
        metricHint.textContent = '';
        return;
    }

    // Find metric details
    const metric = availableMetrics.find(m => m.value === selectedMetric);
    if (metric) {
        metricHint.textContent = metric.description;
    }

    // Add applicable dimensions
    const applicableDimensions = availableDimensions.filter(dim =>
        dim.applicableTo.includes(selectedMetric)
    );

    applicableDimensions.forEach(dim => {
        const option = document.createElement('option');
        option.value = dim.value;
        option.textContent = dim.label;
        groupBySelect.appendChild(option);
    });
}

// Load filter dropdown options (universities, projects, teams)
async function loadFilterOptions() {
    try {
        const [universitiesResp, projectsResp, teamsResp] = await Promise.all([
            fetch(`${API_BASE_URL}/universities`),
            fetch(`${API_BASE_URL}/projects`),
            fetch(`${API_BASE_URL}/teams`)
        ]);

        universities = await universitiesResp.json();
        projects = await projectsResp.json();
        teams = await teamsResp.json();

        // Populate filter dropdowns
        const uniSelect = document.getElementById('filterUniversity');
        universities.forEach(uni => {
            const option = document.createElement('option');
            option.value = uni.id;
            option.textContent = uni.name;
            uniSelect.appendChild(option);
        });

        const projSelect = document.getElementById('filterProject');
        projects.forEach(proj => {
            const option = document.createElement('option');
            option.value = proj.id;
            option.textContent = proj.name;
            projSelect.appendChild(option);
        });

        const teamSelect = document.getElementById('filterTeam');
        teams.forEach(team => {
            const option = document.createElement('option');
            option.value = team.id;
            option.textContent = team.name;
            teamSelect.appendChild(option);
        });
    } catch (error) {
        console.error('Error loading filter options:', error);
    }
}

// Setup event listeners
function setupEventListeners() {
    document.getElementById('metricSelect').addEventListener('change', updateGroupByOptions);
    document.getElementById('updateChartBtn').addEventListener('click', updateChart);

    // Auto-suggest chart type based on metric
    document.getElementById('metricSelect').addEventListener('change', () => {
        const metric = document.getElementById('metricSelect').value;
        const chartTypeSelect = document.getElementById('chartTypeSelect');

        // Smart defaults
        if (metric === 'status_distribution' || metric === 'students_by_status_and_expertise') {
            chartTypeSelect.value = 'doughnut';
        } else if (metric === 'avg_terms_remaining') {
            chartTypeSelect.value = 'bar';
        }
    });
}

// Update chart with new data
async function updateChart() {
    const metric = document.getElementById('metricSelect').value;
    const groupBy = document.getElementById('groupBySelect').value;
    const chartType = document.getElementById('chartTypeSelect').value;

    if (!metric) {
        showError('Please select a metric to visualize');
        return;
    }

    // Show loading spinner
    document.getElementById('loadingSpinner').classList.add('active');
    document.getElementById('errorMessage').classList.remove('active');

    // Build filters
    const filters = {};
    const filterUni = document.getElementById('filterUniversity').value;
    const filterProj = document.getElementById('filterProject').value;
    const filterTeam = document.getElementById('filterTeam').value;

    if (filterUni) filters.university_id = filterUni;
    if (filterProj) filters.project_id = filterProj;
    if (filterTeam) filters.team_id = filterTeam;

    // Fetch data
    try {
        const response = await fetch(`${API_BASE_URL}/analytics/data`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                metric: metric,
                groupBy: groupBy || null,
                filters: filters
            })
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.error || 'Failed to fetch data');
        }

        const result = await response.json();

        // Hide loading spinner
        document.getElementById('loadingSpinner').classList.remove('active');

        // Render chart
        renderChart(result, chartType);
        updateChartTitle(metric, groupBy, filters);
        generateInsights(result);

    } catch (error) {
        console.error('Error fetching analytics data:', error);
        document.getElementById('loadingSpinner').classList.remove('active');
        showError(error.message);
    }
}

// Render chart using Chart.js
function renderChart(data, chartType) {
    const canvas = document.getElementById('analyticsChart');

    // Destroy existing chart
    if (chart) {
        chart.destroy();
    }

    // Handle cross-tabulation data differently
    if (data.metric === 'students_by_status_and_expertise') {
        renderCrossTabulation(data.data, chartType);
        return;
    }

    // Extract labels and values
    const labels = data.data.map(d => d.label);
    const values = data.data.map(d => d.value);

    // Color schemes
    const backgroundColors = [
        'rgba(0, 240, 255, 0.8)',    // Cyan
        'rgba(124, 58, 237, 0.8)',   // Purple
        'rgba(236, 72, 153, 0.8)',   // Pink
        'rgba(251, 191, 36, 0.8)',   // Yellow
        'rgba(16, 185, 129, 0.8)',   // Green
        'rgba(239, 68, 68, 0.8)',    // Red
        'rgba(59, 130, 246, 0.8)',   // Blue
        'rgba(245, 158, 11, 0.8)',   // Orange
    ];

    const borderColors = backgroundColors.map(color => color.replace('0.8', '1'));

    // Chart configuration
    const config = {
        type: chartType,
        data: {
            labels: labels,
            datasets: [{
                label: data.metric.replace(/_/g, ' ').toUpperCase(),
                data: values,
                backgroundColor: backgroundColors,
                borderColor: borderColors,
                borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    display: chartType === 'pie' || chartType === 'doughnut',
                    labels: {
                        color: '#9ca3af',
                        font: {
                            family: 'Space Grotesk',
                            size: 12
                        }
                    }
                },
                title: {
                    display: false
                }
            },
            scales: chartType !== 'pie' && chartType !== 'doughnut' && chartType !== 'radar' ? {
                y: {
                    beginAtZero: true,
                    ticks: {
                        color: '#9ca3af'
                    },
                    grid: {
                        color: 'rgba(255, 255, 255, 0.05)'
                    }
                },
                x: {
                    ticks: {
                        color: '#9ca3af'
                    },
                    grid: {
                        color: 'rgba(255, 255, 255, 0.05)'
                    }
                }
            } : {}
        }
    };

    chart = new Chart(canvas, config);
}

// Render cross-tabulation (grouped bar chart)
function renderCrossTabulation(data, chartType) {
    const canvas = document.getElementById('analyticsChart');

    if (chart) {
        chart.destroy();
    }

    // Group data by status
    const statuses = [...new Set(data.map(d => d.status))];
    const expertises = [...new Set(data.map(d => d.expertise))];

    const datasets = statuses.map((status, idx) => {
        const statusData = expertises.map(expertise => {
            const item = data.find(d => d.status === status && d.expertise === expertise);
            return item ? item.value : 0;
        });

        const colors = [
            'rgba(0, 240, 255, 0.8)',    // Cyan
            'rgba(124, 58, 237, 0.8)',   // Purple
            'rgba(236, 72, 153, 0.8)',   // Pink
        ];

        return {
            label: status.toUpperCase(),
            data: statusData,
            backgroundColor: colors[idx % colors.length],
            borderColor: colors[idx % colors.length].replace('0.8', '1'),
            borderWidth: 2
        };
    });

    const config = {
        type: 'bar',
        data: {
            labels: expertises,
            datasets: datasets
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    display: true,
                    labels: {
                        color: '#9ca3af',
                        font: {
                            family: 'Space Grotesk'
                        }
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: { color: '#9ca3af' },
                    grid: { color: 'rgba(255, 255, 255, 0.05)' }
                },
                x: {
                    ticks: { color: '#9ca3af' },
                    grid: { color: 'rgba(255, 255, 255, 0.05)' }
                }
            }
        }
    };

    chart = new Chart(canvas, config);
}

// Update chart title based on selection
function updateChartTitle(metric, groupBy, filters) {
    const metricObj = availableMetrics.find(m => m.value === metric);
    const dimensionObj = availableDimensions.find(d => d.value === groupBy);

    let title = metricObj ? metricObj.label : 'Analytics';

    if (groupBy && dimensionObj) {
        title += ` by ${dimensionObj.label}`;
    }

    document.getElementById('chartTitle').textContent = title;

    // Build subtitle with active filters
    let subtitle = '';
    if (filters.university_id) {
        const uni = universities.find(u => u.id === filters.university_id);
        subtitle += `University: ${uni ? uni.name : filters.university_id}`;
    }
    if (filters.project_id) {
        const proj = projects.find(p => p.id === filters.project_id);
        if (subtitle) subtitle += ' • ';
        subtitle += `Project: ${proj ? proj.name : filters.project_id}`;
    }

    document.getElementById('chartSubtitle').textContent = subtitle;
}

// Generate insights based on data
function generateInsights(result) {
    const insightsPanel = document.getElementById('insightsPanel');
    const data = result.data;

    if (!data || data.length === 0) {
        insightsPanel.innerHTML = '<p class="hint">No data available for the selected criteria.</p>';
        return;
    }

    let insights = '<ul style="color: var(--text-secondary); line-height: 1.8;">';

    // Calculate total
    const total = data.reduce((sum, item) => sum + (item.value || 0), 0);
    insights += `<li><strong>Total:</strong> ${total.toFixed(2)}</li>`;

    // Find highest and lowest
    const sorted = [...data].sort((a, b) => b.value - a.value);
    if (sorted.length > 0) {
        insights += `<li><strong>Highest:</strong> ${sorted[0].label} (${sorted[0].value})</li>`;
        if (sorted.length > 1) {
            insights += `<li><strong>Lowest:</strong> ${sorted[sorted.length - 1].label} (${sorted[sorted.length - 1].value})</li>`;
        }
    }

    // Calculate average
    const avg = total / data.length;
    insights += `<li><strong>Average:</strong> ${avg.toFixed(2)}</li>`;

    insights += '</ul>';

    insightsPanel.innerHTML = insights;
}

// Show error message
function showError(message) {
    const errorDiv = document.getElementById('errorMessage');
    errorDiv.textContent = message;
    errorDiv.classList.add('active');

    setTimeout(() => {
        errorDiv.classList.remove('active');
    }, 5000);
}
