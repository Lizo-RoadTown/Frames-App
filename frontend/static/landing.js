/**
 * FRAMES Landing Page JavaScript
 * Handles portal selection, university selection, role selection, and student code entry
 */

let selectedUniversity = null;
let selectedRole = null;

// Role permissions mapping
const rolePermissions = {
    faculty: ['teams', 'faculty', 'projects', 'connections', 'health', 'compare', 'research'],
    teamlead: ['teams', 'health']
};

// Tile definitions
const tiles = {
    teams: {
        icon: 'users',
        title: 'Student Teams',
        description: 'Add or update your student team structure and expertise areas',
        action: 'manageTeams()'
    },
    faculty: {
        icon: 'graduation-cap',
        title: 'Faculty & Mentors',
        description: 'Add or update faculty advisors, staff, and expert involvement',
        action: 'manageFaculty()'
    },
    projects: {
        icon: 'rocket',
        title: 'Missions & Projects',
        description: 'Add your active missions, including PROVES and local projects',
        action: 'manageProjects()'
    },
    connections: {
        icon: 'link',
        title: 'Connections',
        description: 'Track your program\'s connections between teams, mentors, and other universities',
        action: 'viewConnections()'
    },
    health: {
        icon: 'bar-chart-2',
        title: 'Program Health',
        description: 'View your program\'s overall health and data analytics',
        action: 'viewAnalytics()'
    },
    compare: {
        icon: 'table',
        title: 'Compare with Others',
        description: 'See comparison metrics and statistics across universities',
        action: 'comparePrograms()'
    },
    research: {
        icon: 'star',
        title: 'Bronco Star Research Team',
        description: 'Access advanced multi-university analysis and network visualization tools',
        action: 'openResearchDashboard()',
        special: true
    }
};

// Portal selection functions
function showUniversitySelection() {
    document.getElementById('mainLanding').classList.add('hidden');
    document.getElementById('universitySelection').classList.remove('hidden');
}

function showStudentCodeEntry() {
    document.getElementById('mainLanding').classList.add('hidden');
    document.getElementById('studentCodeEntry').classList.remove('hidden');
    document.getElementById('studentCode').value = '';
    document.getElementById('codeError').style.display = 'none';
}

function backToPortals() {
    // Hide all sections
    document.getElementById('universitySelection').classList.add('hidden');
    document.getElementById('studentCodeEntry').classList.add('hidden');
    document.getElementById('roleSelection').classList.add('hidden');
    document.getElementById('dashboardOptions').classList.add('hidden');
    
    // Show main landing
    document.getElementById('mainLanding').classList.remove('hidden');
    
    // Clear code input
    document.getElementById('studentCode').value = '';
    document.getElementById('codeError').style.display = 'none';
}

function validateStudentCode() {
    const code = document.getElementById('studentCode').value.trim();
    const errorMsg = document.getElementById('codeError');
    
    if (!code) {
        errorMsg.textContent = 'Please enter an access code';
        errorMsg.style.display = 'block';
        return;
    }
    
    // Placeholder validation - TODO: implement actual validation
    // For now, accept any non-empty code
    console.log('Student code entered:', code);
    
    // TODO: Replace with actual backend validation
    errorMsg.textContent = 'Code validation is not yet implemented. Please contact your administrator.';
    errorMsg.style.display = 'block';
    
    // Future implementation:
    // - Send code to backend for validation
    // - On success, redirect to student portal page
    // - On failure, show error message
}

// University selection
document.querySelectorAll('.university-btn').forEach(btn => {
    btn.addEventListener('click', function() {
        selectedUniversity = this.dataset.id;
        const universityName = this.querySelector('.uni-name').textContent;

        // Store in session
        sessionStorage.setItem('selectedUniversity', selectedUniversity);
        sessionStorage.setItem('selectedUniversityName', universityName);

        // Show role selection
        showRoleSelection(universityName);
    });
});

function showRoleSelection(uniName) {
    document.getElementById('mainLanding').classList.add('hidden');
    document.getElementById('roleSelection').classList.remove('hidden');
    document.getElementById('selectedUniNameRole').textContent = uniName;
}

function selectRole(role) {
    selectedRole = role;
    sessionStorage.setItem('selectedRole', role);
    
    const uniName = sessionStorage.getItem('selectedUniversityName');
    showDashboardOptions(uniName, role);
}

function showDashboardOptions(uniName, role) {
    document.getElementById('roleSelection').classList.add('hidden');
    document.getElementById('dashboardOptions').classList.remove('hidden');
    
    // Build dashboard header and tiles based on role
    const permissions = rolePermissions[role];
    const dashboardDiv = document.getElementById('dashboardOptions');
    
    dashboardDiv.innerHTML = `
        <div class="dashboard-header">
            <h2 id="selectedUniName">${uniName}</h2>
            <button class="btn-glow" onclick="changeUniversity()"><span class="lucide" data-lucide="globe"></span> Change University</button>
        </div>
        <div class="options-grid">
            ${permissions.map(tileKey => {
                const tile = tiles[tileKey];
                const specialClass = tile.special ? ' class="research-tile"' : '';
                return `
                    <div class="option-card" onclick="${tile.action}"${specialClass}>
                        <div class="option-icon"><span class="lucide" data-lucide="${tile.icon}"></span></div>
                        <div class="option-content">
                            <h3>${tile.title}</h3>
                            <p>${tile.description}</p>
                        </div>
                    </div>
                `;
            }).join('')}
        </div>
    `;
    
    // Reinitialize Lucide icons
    if (typeof lucide !== 'undefined') {
        lucide.createIcons({ color: '#00f0ff', class: 'lucide-glow' });
    }
}

function changeUniversity() {
    document.getElementById('dashboardOptions').classList.add('hidden');
    document.getElementById('roleSelection').classList.add('hidden');
    document.getElementById('mainLanding').classList.remove('hidden');
    selectedUniversity = null;
    selectedRole = null;
    sessionStorage.removeItem('selectedUniversity');
    sessionStorage.removeItem('selectedUniversityName');
    sessionStorage.removeItem('selectedRole');
}

function viewAllUniversities() {
    window.location.href = '/comparative';
}

function manageTeams() {
    window.location.href = `/students?university=${selectedUniversity}`;
}

function manageFaculty() {
    window.location.href = `/faculty?university=${selectedUniversity}`;
}

function manageProjects() {
    window.location.href = `/projects?university=${selectedUniversity}`;
}

function viewConnections() {
    window.location.href = `/dashboard?university=${selectedUniversity}`;
}

function viewAnalytics() {
    window.location.href = `/dashboard?university=${selectedUniversity}`;
}

function comparePrograms() {
    window.location.href = '/comparative';
}

function viewMultiUniversityNetwork() {
    window.location.href = '/multi-university-network';
}

function openResearchDashboard() {
    window.location.href = '/research';
}

// Check if university and role were previously selected
window.addEventListener('DOMContentLoaded', () => {
    const savedUni = sessionStorage.getItem('selectedUniversity');
    const savedUniName = sessionStorage.getItem('selectedUniversityName');
    const savedRole = sessionStorage.getItem('selectedRole');

    if (savedUni && savedUniName && savedRole) {
        selectedUniversity = savedUni;
        selectedRole = savedRole;
        showDashboardOptions(savedUniName, savedRole);
    } else if (savedUni && savedUniName) {
        selectedUniversity = savedUni;
        showRoleSelection(savedUniName);
    }
});
