/**
 * API Client for FRAMES Backend
 * Handles all communication with Flask REST API
 */

// Always talk to the current origin; no localhost fallback now that DB is hosted
const API_BASE_URL = `${window.location.origin}/api`;

class FramesAPI {
    static async _handleResponse(res) {
        const contentType = res.headers.get('content-type') || '';
        if (!res.ok) {
            // try to parse JSON error, otherwise return text
            if (contentType.includes('application/json')) {
                const err = await res.json();
                throw new Error(err.message || JSON.stringify(err));
            } else {
                const text = await res.text();
                throw new Error(text || `HTTP ${res.status}`);
            }
        }
        if (contentType.includes('application/json')) return await res.json();
        // fallback: return raw text
        return await res.text();
    }
    // ============================================================================
    // Teams
    // ============================================================================

    static async getTeams() {
        const response = await fetch(`${API_BASE_URL}/teams`);
        return await response.json();
    }

    static async createTeam(teamData) {
        const response = await fetch(`${API_BASE_URL}/teams`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(teamData)
        });
        return await response.json();
    }

    static async updateTeam(teamId, teamData) {
        const response = await fetch(`${API_BASE_URL}/teams/${teamId}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(teamData)
        });
        return await response.json();
    }

    static async deleteTeam(teamId) {
        const response = await fetch(`${API_BASE_URL}/teams/${teamId}`, {
            method: 'DELETE'
        });
        return await response.json();
    }

    // ============================================================================
    // Faculty
    // ============================================================================

    static async getFaculty() {
        const response = await fetch(`${API_BASE_URL}/faculty`);
        return await response.json();
    }

    static async createFaculty(facultyData) {
        const response = await fetch(`${API_BASE_URL}/faculty`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(facultyData)
        });
        return await response.json();
    }

    static async deleteFaculty(facultyId) {
        const response = await fetch(`${API_BASE_URL}/faculty/${facultyId}`, {
            method: 'DELETE'
        });
        return await response.json();
    }

    // ============================================================================
    // Projects
    // ============================================================================

    static async getProjects() {
        const response = await fetch(`${API_BASE_URL}/projects`);
        return await response.json();
    }

    static async createProject(projectData) {
        const response = await fetch(`${API_BASE_URL}/projects`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(projectData)
        });
        return await response.json();
    }

    static async deleteProject(projectId) {
        const response = await fetch(`${API_BASE_URL}/projects/${projectId}`, {
            method: 'DELETE'
        });
        return await response.json();
    }

    // ============================================================================
    // Interfaces
    // ============================================================================

    static async getInterfaces() {
        const response = await fetch(`${API_BASE_URL}/interfaces`);
        return await response.json();
    }

    static async createInterface(interfaceData) {
        const response = await fetch(`${API_BASE_URL}/interfaces`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(interfaceData)
        });
        return await response.json();
    }

    static async deleteInterface(interfaceId) {
        const response = await fetch(`${API_BASE_URL}/interfaces/${interfaceId}`, {
            method: 'DELETE'
        });
        return await response.json();
    }

    // ============================================================================
    // System State
    // ============================================================================

    static async getState() {
        const response = await fetch(`${API_BASE_URL}/state`);
        return await response.json();
    }

    static async setState(stateData) {
        const response = await fetch(`${API_BASE_URL}/state`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(stateData)
        });
        return await response.json();
    }

    static async resetState() {
        const response = await fetch(`${API_BASE_URL}/state/reset`, {
            method: 'POST'
        });
        return await response.json();
    }

    static async loadSampleData() {
        const response = await fetch(`${API_BASE_URL}/sample-data`, {
            method: 'POST'
        });
        return await response.json();
    }

    // ============================================================================
    // Analytics
    // ============================================================================

    static async getStatistics() {
        const response = await fetch(`${API_BASE_URL}/analytics/statistics`);
        return await response.json();
    }

    static async getNDADiagnostic() {
        const response = await fetch(`${API_BASE_URL}/analytics/nda-diagnostic`);
        return await response.json();
    }

    static async getBackwardTracing() {
        const response = await fetch(`${API_BASE_URL}/analytics/backward-tracing`);
        return await response.json();
    }

    static async getTeamLifecycle() {
        const response = await fetch(`${API_BASE_URL}/analytics/team-lifecycle`);
        return await response.json();
    }

    // ============================================================================
    // Sandboxes / Play Mode
    // ============================================================================

    static async listSandboxes(universityId) {
        const url = new URL(`${API_BASE_URL}/sandboxes`, window.location.origin);
        if (universityId) url.searchParams.set('university_id', universityId);
        const response = await fetch(url.toString());
        return await response.json();
    }

    static async createSandbox(sandboxData) {
        const response = await fetch(`${API_BASE_URL}/sandboxes`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(sandboxData)
        });
        return await FramesAPI._handleResponse(response);
    }

    static async getSandbox(sandboxId) {
        const response = await fetch(`${API_BASE_URL}/sandboxes/${sandboxId}`);
        return await FramesAPI._handleResponse(response);
    }

    static async updateSandbox(sandboxId, sandboxData) {
        const response = await fetch(`${API_BASE_URL}/sandboxes/${sandboxId}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(sandboxData)
        });
        return await FramesAPI._handleResponse(response);
    }

    static async deleteSandbox(sandboxId) {
        const response = await fetch(`${API_BASE_URL}/sandboxes/${sandboxId}`, {
            method: 'DELETE'
        });
        return await FramesAPI._handleResponse(response);
    }

    static async copyLiveToSandbox(sandboxId) {
        const response = await fetch(`${API_BASE_URL}/sandboxes/${sandboxId}/copy-live`, {
            method: 'POST'
        });
        return await FramesAPI._handleResponse(response);
    }
}

// Export for use in other scripts
window.FramesAPI = FramesAPI;
