/**
 * Student Teams Management
 */

let universityId = null;
let universityName = null;

// Get university from URL or session
function getUniversityInfo() {
    const urlParams = new URLSearchParams(window.location.search);
    const urlUniversity = urlParams.get('university');

    // URL parameter takes precedence over sessionStorage
    if (urlUniversity) {
        universityId = urlUniversity;
        sessionStorage.setItem('selectedUniversity', universityId);
        // Try to get a better name (could be improved with a lookup table)
        universityName = urlUniversity.replace(/([A-Z])/g, ' $1').trim() || 'Your University';
        sessionStorage.setItem('selectedUniversityName', universityName);
    } else {
        universityId = sessionStorage.getItem('selectedUniversity');
        universityName = sessionStorage.getItem('selectedUniversityName') || 'Your University';
    }

    if (!universityId) {
        alert('Please select a university first');
        window.location.href = '/';
        return false;
    }

    document.getElementById('universityName').textContent = universityName;
    return true;
}

// Load available projects for dropdown
async function loadProjects() {
    try {
        const response = await fetch(`${API_BASE_URL}/projects?university_id=${universityId}`);
        const projects = await response.json();

        const projectSelect = document.getElementById('project_id');
        projectSelect.innerHTML = '<option value="">Select project...</option>';

        projects.forEach(project => {
            const option = document.createElement('option');
            option.value = project.id;
            option.textContent = project.name;
            projectSelect.appendChild(option);
        });
    } catch (error) {
        console.error('Error loading projects:', error);
    }
}

// Load existing teams
async function loadTeams() {
    try {
        const [teamsRes, projectsRes] = await Promise.all([
            fetch(`${API_BASE_URL}/teams?university_id=${universityId}`),
            fetch(`${API_BASE_URL}/projects?university_id=${universityId}`)
        ]);

        const teams = await teamsRes.json();
        const projects = await projectsRes.json();

        // Create project lookup
        const projectMap = {};
        projects.forEach(p => projectMap[p.id] = p.name);

        const teamsList = document.getElementById('teamsList');

        if (teams.length === 0) {
            teamsList.innerHTML = '<p class="empty-state">No teams yet. Add your first team below!</p>';
            return;
        }

        teamsList.innerHTML = teams.map(team => `
            <div class="item-card" data-id="${team.id}">
                <div class="item-header">
                    <h3 class="item-title">${team.name}</h3>
                    <div class="item-badges">
                        ${team.project_id && projectMap[team.project_id] ? `<span class="badge badge-project">📦 ${projectMap[team.project_id]}</span>` : ''}
                        ${team.discipline ? `<span class="badge">${formatDiscipline(team.discipline)}</span>` : ''}
                    </div>
                </div>
                ${team.description ? `<p class="item-description">${team.description}</p>` : ''}
                <div class="item-actions">
                    <button class="btn-edit" onclick="editTeam('${team.id}')">Edit</button>
                    <button class="btn-delete" onclick="deleteTeam('${team.id}', '${team.name}')">Delete</button>
                </div>
            </div>
        `).join('');
    } catch (error) {
        console.error('Error loading teams:', error);
        showError('Failed to load teams. Please refresh the page.');
    }
}

// Format helpers
function formatDiscipline(discipline) {
    const map = {
        'electrical': 'Electrical',
        'software': 'Software',
        'mechanical': 'Mechanical',
        'mission-ops': 'Mission Ops',
        'communications': 'Communications',
        'systems': 'Systems',
        'other': 'Other'
    };
    return map[discipline] || discipline;
}

function formatLifecycle(lifecycle) {
    const map = {
        'incoming': 'Incoming',
        'established': 'Established',
        'outgoing': 'Outgoing'
    };
    return map[lifecycle] || lifecycle;
}

// Add new team
document.getElementById('addTeamForm').addEventListener('submit', async (e) => {
    e.preventDefault();

    const formData = new FormData(e.target);
    const projectId = formData.get('project_id');

    if (!projectId) {
        showError('Please select a project for this team');
        return;
    }

    const teamData = {
        university_id: universityId,
        project_id: projectId,
        name: formData.get('name'),
        discipline: formData.get('discipline') || null,
        description: formData.get('description') || null
    };

    try {
        const response = await fetch(`${API_BASE_URL}/teams`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(teamData)
        });

        if (response.ok) {
            showSuccess('Team added successfully!');
            e.target.reset();
            await loadTeams();
        } else {
            const error = await response.json();
            showError(error.message || 'Failed to add team');
        }
    } catch (error) {
        console.error('Error adding team:', error);
        showError('Failed to add team. Please try again.');
    }
});

// Delete team
async function deleteTeam(teamId, teamName) {
    if (!confirm(`Are you sure you want to delete "${teamName}"?`)) {
        return;
    }

    try {
        const response = await fetch(`${API_BASE_URL}/teams/${teamId}`, {
            method: 'DELETE'
        });

        if (response.ok) {
            showSuccess('Team deleted successfully!');
            await loadTeams();
        } else {
            showError('Failed to delete team');
        }
    } catch (error) {
        console.error('Error deleting team:', error);
        showError('Failed to delete team. Please try again.');
    }
}

// Edit team (placeholder for now)
function editTeam(teamId) {
    alert('Edit functionality coming soon! For now, please delete and re-add the team.');
}

// Show messages
function showSuccess(message) {
    const existing = document.querySelector('.success-message');
    if (existing) existing.remove();

    const msg = document.createElement('div');
    msg.className = 'success-message';
    msg.textContent = message;
    document.querySelector('.container').insertBefore(msg, document.querySelector('.card'));

    setTimeout(() => msg.remove(), 3000);
}

function showError(message) {
    const existing = document.querySelector('.error-message');
    if (existing) existing.remove();

    const msg = document.createElement('div');
    msg.className = 'error-message';
    msg.textContent = message;
    document.querySelector('.container').insertBefore(msg, document.querySelector('.card'));

    setTimeout(() => msg.remove(), 5000);
}

// Initialize
window.addEventListener('DOMContentLoaded', () => {
    if (getUniversityInfo()) {
        loadProjects();
        loadTeams();
    }
});
