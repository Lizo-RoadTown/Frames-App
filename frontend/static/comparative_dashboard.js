/**
 * FRAMES Comparative Dashboard - JavaScript
 *
 * Connects the comparative dashboard UI to the multi-university API endpoints.
 * Loads real data from the database and updates the UI dynamically.
 */

// Configuration
const API_BASE = '/api';
const RESEARCHER_MODE = true; // Cal Poly Pomona researcher has full access

// Current state
let dashboardData = null;

/**
 * Initialize dashboard on page load
 */
document.addEventListener('DOMContentLoaded', async () => {
    console.log('FRAMES Comparative Dashboard initializing...');

    // Setup navigation
    setupNavigation();

    // Load initial view (All Universities)
    await loadAllUniversitiesView();
});

/**
 * Setup navigation button handlers
 */
function setupNavigation() {
    document.getElementById('viewAllBtn').addEventListener('click', async () => {
        await switchView('all');
    });

    document.getElementById('viewProvesBtn').addEventListener('click', async () => {
        await switchView('proves');
    });

    document.getElementById('viewOutcomesBtn').addEventListener('click', async () => {
        await switchView('outcomes');
    });
}

/**
 * Switch between views
 */
async function switchView(view) {
    // Update active button
    document.querySelectorAll('nav button').forEach(btn => btn.classList.remove('active'));

    if (view === 'all') {
        document.getElementById('viewAllBtn').classList.add('active');
        await loadAllUniversitiesView();
    } else if (view === 'proves') {
        document.getElementById('viewProvesBtn').classList.add('active');
        await loadProvesView();
    } else if (view === 'outcomes') {
        document.getElementById('viewOutcomesBtn').classList.add('active');
        await loadOutcomesView();
    }
}

/**
 * Load All Universities view with real data
 */
async function loadAllUniversitiesView() {
    try {
        console.log('Loading comparative dashboard data...');

        const response = await fetch(`${API_BASE}/dashboard/comparative`, {
            headers: {
                'X-University-ID': 'CalPolyPomona',
                'X-Is-Researcher': RESEARCHER_MODE ? 'true' : 'false'
            }
        });

        if (!response.ok) {
            throw new Error(`API error: ${response.status}`);
        }

        dashboardData = await response.json();
        console.log('Dashboard data loaded:', dashboardData);

        // Make sure we're showing the universities grid
        document.getElementById('dashboardContent').innerHTML = `
            <section id="allUniversitiesView">
                <h2>All Universities Overview</h2>
                <div id="aggregateMetrics"></div>
                <div class="universities-grid"></div>
            </section>
        `;

        // Update UI with real data
        displayAggregateMetrics(dashboardData.aggregate_metrics);
        updateUniversityCards(dashboardData);

    } catch (error) {
        console.error('Error loading dashboard:', error);
        // Fallback to sample/mock data for demo
        dashboardData = getSampleDashboardData();
        document.getElementById('dashboardContent').innerHTML = `
            <section id="allUniversitiesView">
                <h2>All Universities Overview (Sample Data)</h2>
                <div id="aggregateMetrics"></div>
                <div class="universities-grid"></div>
            </section>
        `;
        displayAggregateMetrics(dashboardData.aggregate_metrics);
        updateUniversityCards(dashboardData);
    }
}

// Sample/mock data for demo fallback
function getSampleDashboardData() {
    return {
        aggregate_metrics: {
            university_count: 8,
            total_teams: 12,
            total_faculty: 6,
            total_projects: 7,
            total_interfaces: 13,
            cross_university_interfaces: 4
        },
        universities: {
            CalPolyPomona: {
                info: { name: 'Cal Poly Pomona', is_lead: true },
                metrics: { team_count: 4, faculty_count: 2, project_count: 2, interface_count: 7 }
            },
            TexasState: {
                info: { name: 'Texas State University', is_lead: false },
                metrics: { team_count: 4, faculty_count: 2, project_count: 2, interface_count: 6 }
            },
            Columbia: {
                info: { name: 'Columbia University', is_lead: false },
                metrics: { team_count: 4, faculty_count: 2, project_count: 2, interface_count: 6 }
            },
            Uni_D: {
                info: { name: 'University D', is_lead: false },
                metrics: { team_count: 0, faculty_count: 0, project_count: 0, interface_count: 0 }
            },
            Uni_E: {
                info: { name: 'University E', is_lead: false },
                metrics: { team_count: 0, faculty_count: 0, project_count: 0, interface_count: 0 }
            },
            Uni_F: {
                info: { name: 'University F', is_lead: false },
                metrics: { team_count: 0, faculty_count: 0, project_count: 0, interface_count: 0 }
            },
            Uni_G: {
                info: { name: 'University G', is_lead: false },
                metrics: { team_count: 0, faculty_count: 0, project_count: 0, interface_count: 0 }
            },
            Uni_H: {
                info: { name: 'University H', is_lead: false },
                metrics: { team_count: 0, faculty_count: 0, project_count: 0, interface_count: 0 }
            }
        }
    };
}

/**
 * Display aggregate metrics
 */
function displayAggregateMetrics(metrics) {
    const container = document.getElementById('aggregateMetrics');
    container.innerHTML = `
        <div class="aggregate-metrics">
            <h3>Collaborative Network Summary</h3>
            <div class="aggregate-grid">
                <div class="agg-metric">
                    <span class="agg-label">Universities</span>
                    <span class="agg-value">${metrics.university_count || 0}</span>
                </div>
                <div class="agg-metric">
                    <span class="agg-label">Total Teams</span>
                    <span class="agg-value">${metrics.total_teams || 0}</span>
                </div>
                <div class="agg-metric">
                    <span class="agg-label">Total Faculty</span>
                    <span class="agg-value">${metrics.total_faculty || 0}</span>
                </div>
                <div class="agg-metric">
                    <span class="agg-label">Total Projects</span>
                    <span class="agg-value">${metrics.total_projects || 0}</span>
                </div>
                <div class="agg-metric">
                    <span class="agg-label">Total Interfaces</span>
                    <span class="agg-value">${metrics.total_interfaces || 0}</span>
                </div>
                <div class="agg-metric highlight">
                    <span class="agg-label">Cross-University Links</span>
                    <span class="agg-value">${metrics.cross_university_interfaces || 0}</span>
                </div>
            </div>
        </div>
    `;
}

/**
 * Update university cards with real data
 */
function updateUniversityCards(data) {
    const grid = document.querySelector('.universities-grid');
    grid.innerHTML = '';

    const { universities } = data;

    for (const [uniId, uniData] of Object.entries(universities)) {
        const isLead = uniData.info.is_lead;
        const metrics = uniData.metrics;

        const card = document.createElement('div');
        card.className = 'university-card';
        card.setAttribute('data-university-id', uniId);

        card.innerHTML = `
            <div class="university-header ${isLead ? 'lead' : ''}">
                <h3>${uniData.info.name}</h3>
                ${isLead ? '<span class="lead-badge">Lead Institution</span>' : ''}
            </div>
            <div class="university-metrics">
                <div class="metric">
                    <span class="metric-label">Teams</span>
                    <span class="metric-value">${metrics.team_count || 0}</span>
                </div>
                <div class="metric">
                    <span class="metric-label">Faculty</span>
                    <span class="metric-value">${metrics.faculty_count || 0}</span>
                </div>
                <div class="metric">
                    <span class="metric-label">Projects</span>
                    <span class="metric-value">${metrics.project_count || 0}</span>
                </div>
                <div class="metric">
                    <span class="metric-label">Interfaces</span>
                    <span class="metric-value">${metrics.interface_count || 0}</span>
                </div>
            </div>
            <div class="university-visualization">
                <div class="viz-placeholder">Molecular Visualization</div>
            </div>
            <div class="university-actions">
                <button class="btn-view-detail">View Details</button>
            </div>
        `;

        // Add click handler
        const btn = card.querySelector('.btn-view-detail');
        btn.onclick = () => viewUniversityDetails(uniId, uniData);

        grid.appendChild(card);
    }
}

/**
 * Load PROVES collaboration view
 */
async function loadProvesView() {
    try {
        const response = await fetch(`${API_BASE}/dashboard/proves`, {
            headers: {
                'X-University-ID': 'CalPolyPomona',
                'X-Is-Researcher': 'true'
            }
        });

        if (!response.ok) throw new Error(`API error: ${response.status}`);

        const data = await response.json();

        document.getElementById('dashboardContent').innerHTML = `
            <section id="provesView">
                <h2>PROVES Collaborative Mission</h2>
                <div class="proves-info">
                    <h3>${data.project.name}</h3>
                    <p>${data.project.description}</p>
                </div>
                <div class="proves-metrics">
                    <div class="metric"><span>Universities</span><strong>${data.metrics.university_count}</strong></div>
                    <div class="metric"><span>Teams</span><strong>${data.metrics.team_count}</strong></div>
                    <div class="metric"><span>Interfaces</span><strong>${data.metrics.interface_count}</strong></div>
                </div>
                <h3>Participating Teams</h3>
                <div class="proves-teams">
                    ${data.participating_teams.map(t => `
                        <div class="team-card">
                            <h4>${t.name}</h4>
                            <p>University: ${t.university_id}</p>
                            <p>Size: ${t.size} | Experience: ${t.experience} months</p>
                        </div>
                    `).join('')}
                </div>
            </section>
        `;
    } catch (error) {
        console.error('Error loading PROVES:', error);
        showError('Failed to load PROVES data.');
    }
}

/**
 * Load outcomes view
 */
async function loadOutcomesView() {
    try {
        const response = await fetch(`${API_BASE}/outcomes`, {
            headers: {
                'X-University-ID': 'CalPolyPomona',
                'X-Is-Researcher': 'true'
            }
        });

        if (!response.ok) throw new Error(`API error: ${response.status}`);

        const outcomes = await response.json();

        document.getElementById('dashboardContent').innerHTML = `
            <section id="outcomesView">
                <h2>Mission & Program Outcomes</h2>
                ${outcomes.length === 0 ?
                    '<p class="no-data">No outcomes recorded yet.</p>' :
                    outcomes.map(o => `
                        <div class="outcome-item ${o.success ? 'success' : 'failure'}">
                            <strong>${o.university_id}</strong>: ${o.outcome_type} -
                            ${o.success ? '✓ Success' : '✗ Failed'}
                            ${o.notes ? `<br><small>${o.notes}</small>` : ''}
                        </div>
                    `).join('')
                }
            </section>
        `;
    } catch (error) {
        console.error('Error loading outcomes:', error);
        showError('Failed to load outcomes.');
    }
}

/**
 * View university details
 */
function viewUniversityDetails(uniId, uniData) {
    alert(`${uniData.info.name}\n\nTeams: ${uniData.metrics.team_count}\nFaculty: ${uniData.metrics.faculty_count}\nProjects: ${uniData.metrics.project_count}\nInterfaces: ${uniData.metrics.interface_count}`);
}

/**
 * Show error message
 */
function showError(message) {
    document.getElementById('dashboardContent').innerHTML = `
        <div class="error-message">
            <h3>Error</h3>
            <p>${message}</p>
            <button onclick="location.reload()">Reload</button>
        </div>
    `;
}
