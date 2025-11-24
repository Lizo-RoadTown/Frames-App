/**
 * FRAMES Research Dashboard
 * Factor configuration, model creation, and validation
 */

let allFactors = [];
let allModels = [];
let universities = [];

// Initialize on page load
window.addEventListener('DOMContentLoaded', async () => {
    setupTabs();
    await loadFactors();
    await loadModels();
    await loadUniversities();
    setupEventListeners();
});

// Tab Management
function setupTabs() {
    const tabs = document.querySelectorAll('.tab');
    const tabContents = document.querySelectorAll('.tab-content');

    tabs.forEach(tab => {
        tab.addEventListener('click', () => {
            const targetTab = tab.dataset.tab;

            // Remove active class from all tabs and contents
            tabs.forEach(t => t.classList.remove('active'));
            tabContents.forEach(tc => tc.classList.remove('active'));

            // Add active class to clicked tab and corresponding content
            tab.classList.add('active');
            document.getElementById(`${targetTab}-tab`).classList.add('active');

            // Re-render icons
            lucide.createIcons({ color: '#00f0ff', class: 'lucide-glow' });
        });
    });
}

// Event Listeners
function setupEventListeners() {
    // Add Factor
    document.getElementById('btn-add-factor').addEventListener('click', () => {
        openModal('modal-add-factor');
    });

    document.getElementById('btn-add-value').addEventListener('click', addFactorValueField);

    document.getElementById('form-add-factor').addEventListener('submit', async (e) => {
        e.preventDefault();
        await createFactor();
    });

    // Create Model
    document.getElementById('btn-create-model').addEventListener('click', () => {
        populateModelFactorsForm();
        openModal('modal-create-model');
    });

    document.getElementById('form-create-model').addEventListener('submit', async (e) => {
        e.preventDefault();
        await createModel();
    });

    // Energy Calculator
    document.getElementById('btn-calculate-network').addEventListener('click', calculateNetworkEnergy);

    // Model Comparison
    document.getElementById('btn-compare-models').addEventListener('click', compareModels);
}

// ============================================================================
// Factor Management
// ============================================================================

async function loadFactors() {
    try {
        const response = await fetch(`${API_BASE_URL}/research/factors`);
        allFactors = await response.json();
        renderFactorsTable();
    } catch (error) {
        console.error('Error loading factors:', error);
        showError('Failed to load risk factors');
    }
}

function renderFactorsTable() {
    const tbody = document.getElementById('factors-tbody');

    if (allFactors.length === 0) {
        tbody.innerHTML = `
            <tr>
                <td colspan="5" style="text-align: center; padding: 2rem; color: var(--text-tertiary);">
                    No risk factors defined yet. Click "Add Factor" to create one.
                </td>
            </tr>
        `;
        return;
    }

    tbody.innerHTML = allFactors.map(factor => `
        <tr>
            <td>
                <strong>${factor.display_name}</strong><br>
                <small style="color: var(--text-tertiary);">${factor.factor_name}</small>
                ${factor.description ? `<br><small class="hint">${factor.description}</small>` : ''}
            </td>
            <td>${factor.category.replace(/_/g, ' ')}</td>
            <td>
                <span class="badge badge-${factor.confidence_level}">
                    ${factor.confidence_level}
                </span>
            </td>
            <td>
                <small>${factor.values ? factor.values.length : 0} values</small>
            </td>
            <td>
                <button class="btn-icon" onclick="viewFactorDetails(${factor.id})" title="View Details">
                    <span class="lucide" data-lucide="eye"></span>
                </button>
                <button class="btn-icon" onclick="editFactor(${factor.id})" title="Edit">
                    <span class="lucide" data-lucide="edit"></span>
                </button>
            </td>
        </tr>
    `).join('');

    lucide.createIcons({ color: '#00f0ff', class: 'lucide-glow' });
}

function addFactorValueField() {
    const container = document.getElementById('factor-values-container');
    const newField = document.createElement('div');
    newField.className = 'factor-value-item';
    newField.innerHTML = `
        <input type="text" class="form-input value-name" placeholder="Value name" required>
        <input type="text" class="form-input value-display" placeholder="Display name" required>
        <input type="number" class="form-input value-contribution" placeholder="0.00-1.00" step="0.01" min="0" max="1" required>
        <button type="button" class="btn-icon" onclick="removeFactorValue(this)">
            <span class="lucide" data-lucide="trash-2"></span>
        </button>
    `;
    container.appendChild(newField);
    lucide.createIcons({ color: '#00f0ff', class: 'lucide-glow' });
}

function removeFactorValue(button) {
    const container = document.getElementById('factor-values-container');
    if (container.children.length > 1) {
        button.closest('.factor-value-item').remove();
    } else {
        alert('At least one factor value is required');
    }
}

async function createFactor() {
    try {
        const factorName = document.getElementById('factor-name').value;
        const displayName = document.getElementById('factor-display-name').value;
        const description = document.getElementById('factor-description').value;
        const category = document.getElementById('factor-category').value;
        const confidenceLevel = document.getElementById('factor-confidence').value;

        // Collect factor values
        const valueItems = document.querySelectorAll('.factor-value-item');
        const values = Array.from(valueItems).map((item, index) => ({
            value_name: item.querySelector('.value-name').value,
            display_name: item.querySelector('.value-display').value,
            energy_loss_contribution: parseFloat(item.querySelector('.value-contribution').value),
            sort_order: index
        }));

        const response = await fetch(`${API_BASE_URL}/research/factors`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                factor_name: factorName,
                display_name: displayName,
                description: description,
                category: category,
                confidence_level: confidenceLevel,
                values: values
            })
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.error || 'Failed to create factor');
        }

        closeModal('modal-add-factor');
        document.getElementById('form-add-factor').reset();
        await loadFactors();
        showSuccess('Risk factor created successfully');
    } catch (error) {
        console.error('Error creating factor:', error);
        alert('Error: ' + error.message);
    }
}

function viewFactorDetails(factorId) {
    const factor = allFactors.find(f => f.id === factorId);
    if (!factor) return;

    const detailsHtml = `
        <div class="card">
            <h3>${factor.display_name}</h3>
            <p><strong>Factor Name:</strong> ${factor.factor_name}</p>
            <p><strong>Category:</strong> ${factor.category}</p>
            <p><strong>Confidence Level:</strong> <span class="badge badge-${factor.confidence_level}">${factor.confidence_level}</span></p>
            ${factor.description ? `<p><strong>Description:</strong> ${factor.description}</p>` : ''}

            <h4 style="margin-top: 1.5rem;">Factor Values</h4>
            <table class="factor-table">
                <thead>
                    <tr>
                        <th>Value</th>
                        <th>Display Name</th>
                        <th>Energy Contribution</th>
                    </tr>
                </thead>
                <tbody>
                    ${factor.values.map(v => `
                        <tr>
                            <td>${v.value_name}</td>
                            <td>${v.display_name}</td>
                            <td>${(v.energy_loss_contribution * 100).toFixed(1)}%</td>
                        </tr>
                    `).join('')}
                </tbody>
            </table>
        </div>
    `;

    // Could open a modal or expand inline - for now, alert
    alert('Factor details view - to be implemented with modal');
}

function editFactor(factorId) {
    // To be implemented
    alert('Edit factor functionality - to be implemented');
}

// ============================================================================
// Model Management
// ============================================================================

async function loadModels() {
    try {
        const response = await fetch(`${API_BASE_URL}/research/models`);
        allModels = await response.json();
        renderModels();
        populateModelSelectors();
    } catch (error) {
        console.error('Error loading models:', error);
        showError('Failed to load models');
    }
}

function renderModels() {
    const container = document.getElementById('models-container');

    if (allModels.length === 0) {
        container.innerHTML = `
            <p style="text-align: center; padding: 2rem; color: var(--text-tertiary);">
                No models created yet. Click "Create Model" to start.
            </p>
        `;
        return;
    }

    container.innerHTML = allModels.map(model => `
        <div class="model-card ${model.is_active ? 'active' : ''}">
            <div class="model-header">
                <div>
                    <h3 class="model-title">${model.display_name}</h3>
                    <small style="color: var(--text-tertiary);">${model.model_name}</small>
                    ${model.is_active ? '<span class="badge badge-active" style="margin-left: 1rem;">ACTIVE</span>' : ''}
                    ${model.is_baseline ? '<span class="badge badge-established" style="margin-left: 0.5rem;">BASELINE</span>' : ''}
                </div>
                <div class="model-actions">
                    ${!model.is_active ? `
                        <button class="btn-icon" onclick="activateModel(${model.id})" title="Activate Model">
                            <span class="lucide" data-lucide="check-circle"></span>
                        </button>
                    ` : ''}
                    <button class="btn-icon" onclick="editModelWeights(${model.id})" title="Edit Weights">
                        <span class="lucide" data-lucide="sliders"></span>
                    </button>
                </div>
            </div>

            ${model.hypothesis ? `<p class="hint"><strong>Hypothesis:</strong> ${model.hypothesis}</p>` : ''}

            <div style="margin-top: 1rem;">
                <strong>Factors (${model.factors.length}):</strong>
                <div style="margin-top: 0.5rem;">
                    ${model.factors.map(f => `
                        <div style="display: flex; justify-content: space-between; padding: 0.5rem; background: var(--bg-secondary); border-radius: 6px; margin-bottom: 0.5rem;">
                            <span>${f.display_name}</span>
                            <span style="color: var(--cyan); font-weight: 600;">×${f.weight.toFixed(2)}</span>
                        </div>
                    `).join('')}
                </div>
            </div>
        </div>
    `).join('');

    lucide.createIcons({ color: '#00f0ff', class: 'lucide-glow' });
}

function populateModelFactorsForm() {
    const container = document.getElementById('model-factors-container');
    container.innerHTML = allFactors.map(factor => `
        <div class="weight-slider-container">
            <div class="weight-slider-label">
                <span>
                    <input type="checkbox" id="factor-${factor.id}" checked>
                    <label for="factor-${factor.id}">${factor.display_name}</label>
                </span>
                <span id="weight-value-${factor.id}">1.00</span>
            </div>
            <input type="range" class="weight-slider" id="weight-${factor.id}"
                   min="0" max="2" step="0.1" value="1.0"
                   oninput="document.getElementById('weight-value-${factor.id}').textContent = this.value">
        </div>
    `).join('');
}

async function createModel() {
    try {
        const modelName = document.getElementById('model-name').value;
        const displayName = document.getElementById('model-display-name').value;
        const hypothesis = document.getElementById('model-hypothesis').value;

        // Collect enabled factors with weights
        const factors = [];
        allFactors.forEach(factor => {
            const checkbox = document.getElementById(`factor-${factor.id}`);
            const weightSlider = document.getElementById(`weight-${factor.id}`);

            if (checkbox.checked) {
                factors.push({
                    factor_id: factor.id,
                    weight: parseFloat(weightSlider.value),
                    enabled: true
                });
            }
        });

        const response = await fetch(`${API_BASE_URL}/research/models`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                model_name: modelName,
                display_name: displayName,
                hypothesis: hypothesis,
                is_active: false,
                factors: factors
            })
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.error || 'Failed to create model');
        }

        closeModal('modal-create-model');
        document.getElementById('form-create-model').reset();
        await loadModels();
        showSuccess('Model created successfully');
    } catch (error) {
        console.error('Error creating model:', error);
        alert('Error: ' + error.message);
    }
}

async function activateModel(modelId) {
    if (!confirm('This will set this model as the active model used by the Operations Dashboard. Continue?')) {
        return;
    }

    try {
        const response = await fetch(`${API_BASE_URL}/research/models/${modelId}/activate`, {
            method: 'POST'
        });

        if (!response.ok) {
            throw new Error('Failed to activate model');
        }

        await loadModels();
        showSuccess('Model activated successfully');
    } catch (error) {
        console.error('Error activating model:', error);
        alert('Error: ' + error.message);
    }
}

function editModelWeights(modelId) {
    // To be implemented - modal with weight sliders
    alert('Edit model weights - to be implemented');
}

// ============================================================================
// Energy Calculator
// ============================================================================

async function loadUniversities() {
    try {
        const response = await fetch(`${API_BASE_URL}/universities`);
        universities = await response.json();

        // Populate university selectors
        const selectors = [
            document.getElementById('calc-university-select'),
            document.getElementById('comparison-university')
        ];

        selectors.forEach(select => {
            if (select) {
                universities.forEach(uni => {
                    const option = document.createElement('option');
                    option.value = uni.id;
                    option.textContent = uni.name;
                    select.appendChild(option);
                });
            }
        });
    } catch (error) {
        console.error('Error loading universities:', error);
    }
}

function populateModelSelectors() {
    const selector = document.getElementById('calc-model-select');
    selector.innerHTML = '<option value="">Select a model...</option>';

    allModels.forEach(model => {
        const option = document.createElement('option');
        option.value = model.id;
        option.textContent = `${model.display_name}${model.is_active ? ' (ACTIVE)' : ''}`;
        selector.appendChild(option);
    });

    // Populate comparison checkboxes
    const checkboxContainer = document.getElementById('comparison-model-checkboxes');
    checkboxContainer.innerHTML = allModels.map(model => `
        <div style="padding: 0.75rem; background: var(--bg-secondary); border-radius: 6px; margin-bottom: 0.5rem;">
            <input type="checkbox" id="compare-model-${model.id}" value="${model.id}">
            <label for="compare-model-${model.id}" style="margin-left: 0.5rem;">
                ${model.display_name}
                ${model.is_active ? '<span class="badge badge-active" style="margin-left: 0.5rem;">ACTIVE</span>' : ''}
            </label>
        </div>
    `).join('');
}

async function calculateNetworkEnergy() {
    try {
        const modelId = document.getElementById('calc-model-select').value;
        const universityId = document.getElementById('calc-university-select').value;

        if (!modelId) {
            alert('Please select a model');
            return;
        }

        const params = new URLSearchParams();
        if (modelId) params.append('model_id', modelId);
        if (universityId) params.append('university_id', universityId);

        const response = await fetch(`${API_BASE_URL}/research/energy/network?${params}`);
        const result = await response.json();

        renderCalculationResults(result);
    } catch (error) {
        console.error('Error calculating energy:', error);
        alert('Error: ' + error.message);
    }
}

function renderCalculationResults(result) {
    const container = document.getElementById('calculation-results');

    const avgPercent = result.average_energy_loss_percent;
    const riskLevel = avgPercent < 15 ? 'low' : avgPercent < 35 ? 'moderate' : avgPercent < 60 ? 'high' : 'critical';
    const riskColor = avgPercent < 15 ? '#10b981' : avgPercent < 35 ? '#fbbf24' : avgPercent < 60 ? '#f59e0b' : '#ef4444';

    container.innerHTML = `
        <div class="energy-result">
            <h3>Network Energy Analysis</h3>

            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem; margin: 1.5rem 0;">
                <div class="stat-card">
                    <div class="stat-value">${result.analyzed_interfaces}</div>
                    <div class="stat-label">Interfaces Analyzed</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value" style="color: ${riskColor};">${avgPercent}%</div>
                    <div class="stat-label">Avg Energy Loss</div>
                </div>
            </div>

            <div class="energy-bar">
                <div class="energy-indicator" style="left: ${avgPercent}%;">${avgPercent}%</div>
            </div>

            <h4 style="margin-top: 1.5rem;">Risk Distribution</h4>
            <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 1rem; margin-top: 1rem;">
                <div class="stat-card">
                    <div class="stat-value" style="color: #10b981;">${result.risk_distribution.low}</div>
                    <div class="stat-label">Low Risk</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value" style="color: #fbbf24;">${result.risk_distribution.moderate}</div>
                    <div class="stat-label">Moderate</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value" style="color: #f59e0b;">${result.risk_distribution.high}</div>
                    <div class="stat-label">High</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value" style="color: #ef4444;">${result.risk_distribution.critical}</div>
                    <div class="stat-label">Critical</div>
                </div>
            </div>
        </div>
    `;
}

// ============================================================================
// Model Comparison
// ============================================================================

async function compareModels() {
    try {
        const checkboxes = document.querySelectorAll('[id^="compare-model-"]');
        const selectedModelIds = Array.from(checkboxes)
            .filter(cb => cb.checked)
            .map(cb => parseInt(cb.value));

        if (selectedModelIds.length < 2) {
            alert('Please select at least 2 models to compare');
            return;
        }

        const universityId = document.getElementById('comparison-university').value;

        const response = await fetch(`${API_BASE_URL}/research/compare-models`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                model_ids: selectedModelIds,
                university_id: universityId || null
            })
        });

        const result = await response.json();
        renderComparisonResults(result.comparisons);
    } catch (error) {
        console.error('Error comparing models:', error);
        alert('Error: ' + error.message);
    }
}

function renderComparisonResults(comparisons) {
    const container = document.getElementById('comparison-results');

    container.innerHTML = `
        <h3 style="margin-top: 2rem;">Comparison Results</h3>
        <div class="comparison-grid">
            ${comparisons.map(comp => {
                const model = allModels.find(m => m.id === comp.model_id);
                return `
                    <div class="comparison-card">
                        <h4>${model ? model.display_name : 'Model ' + comp.model_id}</h4>

                        <div class="stat-row">
                            <span>Interfaces Analyzed</span>
                            <strong>${comp.analyzed_interfaces}</strong>
                        </div>
                        <div class="stat-row">
                            <span>Avg Energy Loss</span>
                            <strong style="color: var(--cyan);">${comp.average_energy_loss_percent}%</strong>
                        </div>

                        <h5 style="margin-top: 1rem; margin-bottom: 0.5rem;">Risk Distribution</h5>
                        <div class="stat-row">
                            <span>Low Risk</span>
                            <strong style="color: #10b981;">${comp.risk_distribution.low}</strong>
                        </div>
                        <div class="stat-row">
                            <span>Moderate Risk</span>
                            <strong style="color: #fbbf24;">${comp.risk_distribution.moderate}</strong>
                        </div>
                        <div class="stat-row">
                            <span>High Risk</span>
                            <strong style="color: #f59e0b;">${comp.risk_distribution.high}</strong>
                        </div>
                        <div class="stat-row">
                            <span>Critical Risk</span>
                            <strong style="color: #ef4444;">${comp.risk_distribution.critical}</strong>
                        </div>
                    </div>
                `;
            }).join('')}
        </div>
    `;
}

// ============================================================================
// Utility Functions
// ============================================================================

function openModal(modalId) {
    document.getElementById(modalId).classList.add('active');
}

function closeModal(modalId) {
    document.getElementById(modalId).classList.remove('active');
}

function showSuccess(message) {
    // Simple success notification - could be enhanced with a toast component
    alert(message);
}

function showError(message) {
    alert('Error: ' + message);
}
