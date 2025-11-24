/**
 * Faculty & Mentors Management
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

// Load existing faculty
async function loadFaculty() {
    try {
        const response = await fetch(`${API_BASE_URL}/faculty?university_id=${universityId}`);
        const faculty = await response.json();

        const facultyList = document.getElementById('facultyList');

        if (faculty.length === 0) {
            facultyList.innerHTML = '<p class="empty-state">No faculty yet. Add your first faculty member below!</p>';
            return;
        }

        facultyList.innerHTML = faculty.map(person => `
            <div class="item-card" data-id="${person.id}">
                <div class="item-header">
                    <h3 class="item-title">${person.name}</h3>
                    <div class="item-badges">
                        ${person.role ? `<span class="badge">${formatRole(person.role)}</span>` : ''}
                    </div>
                </div>
                ${person.description ? `<p class="item-description">${person.description}</p>` : ''}
                <div class="item-actions">
                    <button class="btn-delete" onclick="deleteFaculty('${person.id}', '${person.name}')">Delete</button>
                </div>
            </div>
        `).join('');
    } catch (error) {
        console.error('Error loading faculty:', error);
        showError('Failed to load faculty. Please refresh the page.');
    }
}

// Format role
function formatRole(role) {
    const map = {
        'faculty-advisor': 'Faculty Advisor',
        'pi': 'Principal Investigator',
        'co-pi': 'Co-PI',
        'staff': 'Staff Engineer',
        'industry-mentor': 'Industry Mentor',
        'jpl-mentor': 'JPL Mentor',
        'other': 'Other'
    };
    return map[role] || role;
}

// Add new faculty
document.getElementById('addFacultyForm').addEventListener('submit', async (e) => {
    e.preventDefault();

    const formData = new FormData(e.target);
    const facultyData = {
        university_id: universityId,
        name: formData.get('name'),
        role: formData.get('role') || null,
        description: formData.get('description') || null
    };

    try {
        const response = await fetch(`${API_BASE_URL}/faculty`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(facultyData)
        });

        if (response.ok) {
            showSuccess('Faculty/mentor added successfully!');
            e.target.reset();
            await loadFaculty();
        } else {
            const error = await response.json();
            showError(error.message || 'Failed to add faculty/mentor');
        }
    } catch (error) {
        console.error('Error adding faculty:', error);
        showError('Failed to add faculty/mentor. Please try again.');
    }
});

// Delete faculty
async function deleteFaculty(facultyId, facultyName) {
    if (!confirm(`Are you sure you want to delete "${facultyName}"?`)) {
        return;
    }

    try {
        const response = await fetch(`${API_BASE_URL}/faculty/${facultyId}`, {
            method: 'DELETE'
        });

        if (response.ok) {
            showSuccess('Faculty/mentor deleted successfully!');
            await loadFaculty();
        } else {
            showError('Failed to delete faculty/mentor');
        }
    } catch (error) {
        console.error('Error deleting faculty:', error);
        showError('Failed to delete faculty/mentor. Please try again.');
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
        loadFaculty();
    }
});
