/**
 * Projects Management
 */

let universityId = null;
let universityName = null;

// Get university from URL or session
function getUniversityInfo() {
    const urlParams = new URLSearchParams(window.location.search);
    universityId = urlParams.get('university') || sessionStorage.getItem('selectedUniversity');
    universityName = sessionStorage.getItem('selectedUniversityName') || 'Your University';

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
        const response = await fetch(`${API_BASE_URL}/projects?university_id=${universityId}`);
        const projects = await response.json();

        const projectsList = document.getElementById('projectsList');

        if (projects.length === 0) {
            projectsList.innerHTML = '<p class="empty-state">No projects yet. Add your first project below!</p>';
            return;
        }

        projectsList.innerHTML = projects.map(project => `
            <div class="item-card" data-id="${project.id}">
                <div class="item-header">
                    <h3 class="item-title">${project.name}</h3>
                    <div class="item-badges">
                        ${project.type ? `<span class="badge">${formatType(project.type)}</span>` : ''}
                        ${project.duration ? `<span class="badge">${project.duration} years</span>` : ''}
                    </div>
                </div>
                ${project.description ? `<p class="item-description">${project.description}</p>` : ''}
                <div class="item-actions">
                    <button class="btn-delete" onclick="deleteProject('${project.id}', '${project.name}')">Delete</button>
                </div>
            </div>
        `).join('');
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
            showSuccess('Project added successfully!');
            e.target.reset();
            await loadProjects();
        } else {
            const error = await response.json();
            showError(error.message || 'Failed to add project');
        }
    } catch (error) {
        console.error('Error adding project:', error);
        showError('Failed to add project. Please try again.');
    }
});

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
