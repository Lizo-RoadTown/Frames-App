/**
 * FRAMES Landing Page JavaScript
 * Handles university selection and navigation
 */

let selectedUniversity = null;

// University selection
document.querySelectorAll('.university-btn').forEach(btn => {
    btn.addEventListener('click', function() {
        selectedUniversity = this.dataset.id;
        const universityName = this.querySelector('.uni-name').textContent;

        // Store in session
        sessionStorage.setItem('selectedUniversity', selectedUniversity);
        sessionStorage.setItem('selectedUniversityName', universityName);

        // Show dashboard options
        showDashboardOptions(universityName);
    });
});

function showDashboardOptions(uniName) {
    document.getElementById('universitySelection').classList.add('hidden');
    document.getElementById('dashboardOptions').classList.remove('hidden');
    document.getElementById('selectedUniName').textContent = uniName;
}

function changeUniversity() {
    document.getElementById('dashboardOptions').classList.add('hidden');
    document.getElementById('universitySelection').classList.remove('hidden');
    selectedUniversity = null;
    sessionStorage.removeItem('selectedUniversity');
    sessionStorage.removeItem('selectedUniversityName');
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
    window.location.href = `/analytics?university=${selectedUniversity}`;
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

// Check if university was previously selected
window.addEventListener('DOMContentLoaded', () => {
    const savedUni = sessionStorage.getItem('selectedUniversity');
    const savedUniName = sessionStorage.getItem('selectedUniversityName');

    if (savedUni && savedUniName) {
        selectedUniversity = savedUni;
        showDashboardOptions(savedUniName);
    }
});
