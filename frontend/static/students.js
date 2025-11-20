/**
 * Student Roster Management
 */

let universityId = null;
let universityName = null;
let allStudents = [];
let teams = [];
let projects = [];

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

// Load teams and projects for dropdowns
async function loadDropdowns() {
    try {
        // Load teams and projects in parallel
        const [teamsResponse, projectsResponse] = await Promise.all([
            fetch(`${API_BASE_URL}/teams?university_id=${universityId}`),
            fetch(`${API_BASE_URL}/projects?university_id=${universityId}`)
        ]);

        teams = await teamsResponse.json();
        projects = await projectsResponse.json();

        // Create project lookup
        const projectMap = {};
        projects.forEach(p => projectMap[p.id] = p);

        const teamSelect = document.getElementById('teamId');
        const filterTeamSelect = document.getElementById('filterTeam');

        teams.forEach(team => {
            const projectName = team.project_id && projectMap[team.project_id]
                ? ` (${projectMap[team.project_id].name})`
                : '';
            const displayName = `${team.name}${projectName}`;

            const option = new Option(displayName, team.id);
            teamSelect.add(option.cloneNode(true));
            filterTeamSelect.add(option);
        });
    } catch (error) {
        console.error('Error loading dropdowns:', error);
    }
}

// Load students
async function loadStudents() {
    try {
        const response = await fetch(`${API_BASE_URL}/students?university_id=${universityId}&active=true`);
        allStudents = await response.json();

        updateSummary();
        filterStudents();
    } catch (error) {
        console.error('Error loading students:', error);
        showError('Failed to load students. Please refresh the page.');
    }
}

// Update summary stats
function updateSummary() {
    const incoming = allStudents.filter(s => s.status === 'incoming').length;
    const established = allStudents.filter(s => s.status === 'established').length;
    const outgoing = allStudents.filter(s => s.status === 'outgoing').length;

    document.getElementById('incomingCount').textContent = incoming;
    document.getElementById('establishedCount').textContent = established;
    document.getElementById('outgoingCount').textContent = outgoing;
}

// Filter students by team
function filterStudents() {
    const teamFilter = document.getElementById('filterTeam').value;

    let filtered = allStudents;

    if (teamFilter) {
        filtered = filtered.filter(s => s.team_id === teamFilter);
    }

    displayStudents(filtered);
}

// Display students
function displayStudents(students) {
    const studentsList = document.getElementById('studentsList');

    if (students.length === 0) {
        studentsList.innerHTML = '<p class="empty-state">No students match the current filters.</p>';
        return;
    }

    studentsList.innerHTML = students.map(student => {
        const team = teams.find(t => t.id === student.team_id);
        const project = team && team.project_id ? projects.find(p => p.id === team.project_id) : null;

        return `
            <div class="item-card" data-id="${student.id}">
                <div class="item-header">
                    <h3 class="item-title">${student.name}</h3>
                    <div class="item-badges">
                        ${student.is_lead ? `<span class="badge" style="background: linear-gradient(135deg, #fbbf24 0%, #f59e0b 100%); color: #0a0a0f;">Team Lead</span>` : ''}
                        ${student.status ? `<span class="badge ${student.status}">${formatStatus(student.status)}</span>` : ''}
                        ${student.expertise_area ? `<span class="badge">${student.expertise_area}</span>` : ''}
                    </div>
                </div>
                <div class="item-details">
                    ${team ? `👥 ${team.name}` : ''}
                    ${project ? `• 🛸 ${project.name}` : ''}
                </div>
                <div class="item-details" style="margin-top: 8px;">
                    <strong>Terms remaining:</strong> ${student.terms_remaining}
                </div>
                <div class="item-actions">
                    <button class="btn-delete" onclick="deleteStudent('${student.id}', '${student.name}')">Remove</button>
                </div>
            </div>
        `;
    }).join('');
}

// Format status
function formatStatus(status) {
    const map = {
        'incoming': 'Incoming',
        'established': 'Established',
        'outgoing': 'Outgoing'
    };
    return map[status] || status;
}

// Add new student
document.getElementById('addStudentForm').addEventListener('submit', async (e) => {
    e.preventDefault();

    const formData = new FormData(e.target);
    const studentData = {
        university_id: universityId,
        name: formData.get('name'),
        team_id: formData.get('team_id'),
        expertise_area: formData.get('expertise_area') || null,
        terms_remaining: parseInt(formData.get('terms_remaining')),
        is_lead: formData.get('is_lead') === 'on'
    };

    try {
        const response = await fetch(`${API_BASE_URL}/students`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(studentData)
        });

        if (response.ok) {
            showSuccess('Student added successfully!');
            e.target.reset();
            // Reset to default
            document.getElementById('termsRemaining').value = 4;
            await loadStudents();
        } else {
            const error = await response.json();
            showError(error.error || 'Failed to add student');
        }
    } catch (error) {
        console.error('Error adding student:', error);
        showError('Failed to add student. Please try again.');
    }
});

// Delete student
async function deleteStudent(studentId, studentName) {
    if (!confirm(`Are you sure you want to remove ${studentName} from the roster?`)) {
        return;
    }

    try {
        const response = await fetch(`${API_BASE_URL}/students/${studentId}`, {
            method: 'DELETE'
        });

        if (response.ok) {
            showSuccess('Student removed successfully!');
            await loadStudents();
        } else {
            showError('Failed to remove student');
        }
    } catch (error) {
        console.error('Error deleting student:', error);
        showError('Failed to remove student. Please try again.');
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
window.addEventListener('DOMContentLoaded', async () => {
    if (getUniversityInfo()) {
        await loadDropdowns();
        await loadStudents();
    }
});
