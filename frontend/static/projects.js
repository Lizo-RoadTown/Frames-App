/**
 * Projects Management
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

// Load existing projects
async function loadProjects() {
    try {
        const [projectsRes, teamsRes] = await Promise.all([
            fetch(`${API_BASE_URL}/projects?university_id=${universityId}`),
            fetch(`${API_BASE_URL}/teams?university_id=${universityId}`)
        ]);

        const projects = await projectsRes.json();
        const allTeams = await teamsRes.json();

        const projectsList = document.getElementById('projectsList');

        if (projects.length === 0) {
            projectsList.innerHTML = '<p class="empty-state">No projects yet. Add your first project below!</p>';
            return;
        }

        projectsList.innerHTML = projects.map(project => {
            const projectTeams = allTeams.filter(t => t.project_id === project.id);
            const teamCount = projectTeams.length;

            return `
                <div class="item-card" data-id="${project.id}">
                    <div class="item-header">
                        <h3 class="item-title">${project.name}</h3>
                        <div class="item-badges">
                            ${project.type ? `<span class="badge">${formatType(project.type)}</span>` : ''}
                            ${project.duration ? `<span class="badge">${project.duration} years</span>` : ''}
                            <span class="badge">👥 ${teamCount} team${teamCount !== 1 ? 's' : ''}</span>
                        </div>
                    </div>
                    ${project.description ? `<p class="item-description">${project.description}</p>` : ''}
                    ${teamCount > 0 ? `
                        <div class="item-details" style="margin-top: 12px;">
                            <strong>Teams:</strong> ${projectTeams.map(t => t.name).join(', ')}
                        </div>
                    ` : ''}
                    <div class="item-actions">
                        <button class="btn-edit" onclick="manageTeams('${project.id}', '${project.name}')">Manage Teams</button>
                        <button class="btn-delete" onclick="deleteProject('${project.id}', '${project.name}')">Delete</button>
                    </div>
                </div>
            `;
        }).join('');
    } catch (error) {
        console.error('Error loading projects:', error);
        showError('Failed to load projects. Please refresh the page.');
    }
}

// Format helpers
function formatType(type) {
    const map = {
        'cubesat': 'CubeSat',
        'jpl-contract': 'JPL Contract',
        'multiversity': 'Multi-University',
        'research': 'Research',
        'competition': 'Competition',
        'other': 'Other'
    };
    return map[type] || type;
}

// Manage teams for a project
async function manageTeams(projectId, projectName) {
    document.getElementById('selectedProjectName').textContent = projectName;
    document.getElementById('teamProjectId').value = projectId;
    document.getElementById('teamsSection').style.display = 'block';

    // Load teams for this project
    await loadProjectTeams(projectId);

    // Scroll to teams section
    document.getElementById('teamsSection').scrollIntoView({ behavior: 'smooth' });
}

function closeTeamsSection() {
    document.getElementById('teamsSection').style.display = 'none';
    document.getElementById('addTeamForm').reset();
}

// Load teams for a specific project
async function loadProjectTeams(projectId) {
    try {
        const response = await fetch(`${API_BASE_URL}/teams?university_id=${universityId}`);
        const allTeams = await response.json();
        const projectTeams = allTeams.filter(t => t.project_id === projectId);

        const teamsList = document.getElementById('projectTeamsList');

        if (projectTeams.length === 0) {
            teamsList.innerHTML = '<p class="empty-state">No teams yet for this project.</p>';
            return;
        }

        teamsList.innerHTML = projectTeams.map(team => `
            <div class="item-card" data-id="${team.id}">
                <div class="item-header">
                    <h3 class="item-title">${team.name}</h3>
                    <div class="item-badges">
                        ${team.discipline ? `<span class="badge">${formatDiscipline(team.discipline)}</span>` : ''}
                    </div>
                </div>
                ${team.description ? `<p class="item-description">${team.description}</p>` : ''}
                <div class="item-actions">
                    <button class="btn-delete" onclick="deleteTeam('${team.id}', '${team.name}')">Delete</button>
                </div>
            </div>
        `).join('');
    } catch (error) {
        console.error('Error loading teams:', error);
    }
}

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

// Add new project
document.getElementById('addProjectForm').addEventListener('submit', async (e) => {
    e.preventDefault();

    const formData = new FormData(e.target);
    const projectData = {
        university_id: universityId,
        name: formData.get('name'),
        type: formData.get('type') || null,
        duration: formData.get('duration') ? parseFloat(formData.get('duration')) : null,
        description: formData.get('description') || null
    };

    try {
        const response = await fetch(`${API_BASE_URL}/projects`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(projectData)
        });

        if (response.ok) {
            const newProject = await response.json();
            showSuccess('Project added successfully! Now add teams to it.');
            e.target.reset();
            await loadProjects();

            // Automatically open the teams section for the new project
            manageTeams(newProject.id, newProject.name);
        } else {
            const error = await response.json();
            showError(error.message || 'Failed to add project');
        }
    } catch (error) {
        console.error('Error adding project:', error);
        showError('Failed to add project. Please try again.');
    }
});

// Add team to project
document.getElementById('addTeamForm').addEventListener('submit', async (e) => {
    e.preventDefault();

    const formData = new FormData(e.target);
    const projectId = formData.get('project_id');

    if (!projectId) {
        showError('No project selected');
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
            document.getElementById('teamProjectId').value = projectId; // Keep project selected
            await loadProjectTeams(projectId);
            await loadProjects(); // Refresh project list to show updated team count
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
            const projectId = document.getElementById('teamProjectId').value;
            if (projectId) {
                await loadProjectTeams(projectId);
            }
            await loadProjects();
        } else {
            showError('Failed to delete team');
        }
    } catch (error) {
        console.error('Error deleting team:', error);
        showError('Failed to delete team. Please try again.');
    }
}

// Delete project
async function deleteProject(projectId, projectName) {
    if (!confirm(`Are you sure you want to delete "${projectName}"?`)) {
        return;
    }

    try {
        const response = await fetch(`${API_BASE_URL}/projects/${projectId}`, {
            method: 'DELETE'
        });

        if (response.ok) {
            showSuccess('Project deleted successfully!');
            closeTeamsSection(); // Close teams section if it was open
            await loadProjects();
        } else {
            showError('Failed to delete project');
        }
    } catch (error) {
        console.error('Error deleting project:', error);
        showError('Failed to delete project. Please try again.');
    }
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
    }
});
