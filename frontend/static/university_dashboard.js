/**
 * University Dashboard JavaScript
 * Shows management tools based on role
 */

let universityId = null;
let universityName = null;
let userRole = null;

// Role permissions mapping
const rolePermissions = {
    faculty: ['teams', 'faculty', 'projects', 'connections', 'health', 'compare'],
    teamlead: ['teams', 'health']
};

// Tile definitions
const tiles = {
    teams: {
        icon: 'users',
        title: 'Student Teams',
        description: 'Add or update your student team structure and expertise areas',
        url: '/students'
    },
    faculty: {
        icon: 'graduation-cap',
        title: 'Faculty & Mentors',
        description: 'Add or update faculty advisors, staff, and expert involvement',
        url: '/faculty'
    },
    projects: {
        icon: 'rocket',
        title: 'Missions & Projects',
        description: 'Add your active missions, including PROVES and local projects',
        url: '/projects'
    },
    connections: {
        icon: 'link',
        title: 'Connections',
        description: 'Track your program\'s connections between teams, mentors, and other universities',
        url: '/dashboard'
    },
    health: {
        icon: 'bar-chart-2',
        title: 'Program Health',
        description: 'View your program\'s overall health and data analytics',
        url: '/dashboard'
    },
    compare: {
        icon: 'table',
        title: 'Compare with Others',
        description: 'See comparison metrics and statistics across universities',
        url: '/comparative'
    },
    research: {
        icon: 'star',
        title: 'Bronco Star Research Team',
        description: 'Access advanced multi-university analysis and network visualization tools',
        url: '/research',
        special: true
    }
};

// Get university and role from URL or session
function getUniversityInfo() {
    const urlParams = new URLSearchParams(window.location.search);
    const urlUniversity = urlParams.get('university');
    const urlRole = urlParams.get('role');

    // URL parameter takes precedence over sessionStorage
    if (urlUniversity) {
        universityId = urlUniversity;
        sessionStorage.setItem('selectedUniversity', universityId);
        universityName = urlUniversity.replace(/([A-Z])/g, ' $1').trim() || 'Your University';
        sessionStorage.setItem('selectedUniversityName', universityName);
    } else {
        universityId = sessionStorage.getItem('selectedUniversity');
        universityName = sessionStorage.getItem('selectedUniversityName') || 'Your University';
    }

    if (urlRole) {
        userRole = urlRole;
        sessionStorage.setItem('selectedRole', userRole);
    } else {
        userRole = sessionStorage.getItem('selectedRole') || 'faculty';
    }

    if (!universityId) {
        alert('Please select a university first');
        window.location.href = '/';
        return false;
    }

    // Update page title
    document.getElementById('universityName').textContent = universityName;
    document.getElementById('universityTitle').textContent = `${universityName} - Program Management`;

    return true;
}

// Build dashboard tiles based on role
function buildDashboard() {
    const permissions = rolePermissions[userRole] || rolePermissions.faculty;
    const toolsGrid = document.getElementById('toolsGrid');

    const tilesHTML = permissions.map(tileKey => {
        const tile = tiles[tileKey];
        const specialStyle = tile.special
            ? ' style="background: linear-gradient(135deg, rgba(124, 58, 237, 0.1) 0%, rgba(192, 38, 211, 0.1) 100%); border: 2px solid rgba(124, 58, 237, 0.3);"'
            : '';
        const iconColor = tile.special ? ' style="color: #c084fc;"' : '';
        const titleColor = tile.special ? ' style="color: #c084fc;"' : '';

        const url = tile.url === '/research'
            ? tile.url
            : `${tile.url}?university=${universityId}`;

        return `
            <div class="option-card" onclick="window.location.href='${url}'"${specialStyle}>
                <div class="option-icon"${iconColor}><span class="lucide" data-lucide="${tile.icon}"></span></div>
                <div class="option-content">
                    <h3${titleColor}>${tile.title}</h3>
                    <p>${tile.description}</p>
                </div>
            </div>
        `;
    }).join('');

    toolsGrid.innerHTML = tilesHTML;

    // Reinitialize Lucide icons
    if (typeof lucide !== 'undefined') {
        lucide.createIcons({ color: '#00f0ff', class: 'lucide-glow' });
    }
}

// Initialize
window.addEventListener('DOMContentLoaded', () => {
    if (getUniversityInfo()) {
        buildDashboard();
    }
});
