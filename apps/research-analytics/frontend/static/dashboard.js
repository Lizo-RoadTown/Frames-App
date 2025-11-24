/**
 * FRAMES 3D Molecular Knowledge Network Visualization
 *
 * Architecture:
 * - PROVES (nucleus) at center
 * - Major projects orbit around PROVES
 * - Teams, faculty, students connect between projects
 * - Animated particle flows show knowledge transfer energy
 * - Color-coded bonds: green (healthy) → yellow → orange → red (critical)
 */

import * as THREE from 'https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.module.js';
import { OrbitControls } from 'https://cdn.jsdelivr.net/npm/three@0.160.0/examples/jsm/controls/OrbitControls.js';

// Global state
let scene, camera, renderer, controls;
let nodes = new Map();
let edges = new Map();
let particles = [];
let selectedNode = null;
let isDragging = false;
let universityId = null;

// Animation
let animationId = null;

// ============================================================================
// Initialization
// ============================================================================

window.addEventListener('DOMContentLoaded', async () => {
    console.log('Dashboard initializing...');

    // Get university from URL
    const urlParams = new URLSearchParams(window.location.search);
    universityId = urlParams.get('university');
    console.log('University ID:', universityId);

    try {
        initScene();
        console.log('Scene initialized');

        await loadNetworkData();
        console.log('Data loaded');

        animate();
        console.log('Animation started');

        setupEventListeners();
        console.log('Event listeners setup complete');
    } catch (error) {
        console.error('Error during initialization:', error);
        document.getElementById('nodeDetails').innerHTML = `
            <p style="color: #ef4444;">Error loading 3D visualization</p>
            <p style="font-size: 0.875rem;">${error.message}</p>
            <p style="font-size: 0.875rem;">Check browser console for details.</p>
        `;
    }
});

function initScene() {
    // Scene
    scene = new THREE.Scene();
    scene.background = new THREE.Color(0x0a0a0f);
    scene.fog = new THREE.Fog(0x0a0a0f, 500, 2000);

    // Camera
    const container = document.getElementById('network');
    camera = new THREE.PerspectiveCamera(
        60,
        container.clientWidth / container.clientHeight,
        1,
        3000
    );
    camera.position.set(0, 300, 600);
    camera.lookAt(0, 0, 0);

    // Renderer
    renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
    renderer.setSize(container.clientWidth, container.clientHeight);
    renderer.setPixelRatio(window.devicePixelRatio);
    container.appendChild(renderer.domElement);

    // Controls
    controls = new OrbitControls(camera, renderer.domElement);
    controls.enableDamping = true;
    controls.dampingFactor = 0.05;
    controls.minDistance = 200;
    controls.maxDistance = 1500;
    controls.autoRotate = true;
    controls.autoRotateSpeed = 0.5;

    // Lights
    const ambientLight = new THREE.AmbientLight(0x404040, 1.5);
    scene.add(ambientLight);

    const pointLight1 = new THREE.PointLight(0x00f0ff, 2, 1000);
    pointLight1.position.set(200, 200, 200);
    scene.add(pointLight1);

    const pointLight2 = new THREE.PointLight(0x8b5cf6, 1.5, 1000);
    pointLight2.position.set(-200, -200, 200);
    scene.add(pointLight2);

    // Resize handler
    window.addEventListener('resize', onWindowResize);
}

function onWindowResize() {
    const container = document.getElementById('network');
    camera.aspect = container.clientWidth / container.clientHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(container.clientWidth, container.clientHeight);
}

// ============================================================================
// Data Loading
// ============================================================================

async function loadNetworkData() {
    try {
        console.log('Loading network data...');
        // Load actual data from API
        const response = await fetch(`${API_BASE_URL}/network-data?university=${universityId || ''}`);

        if (!response.ok) {
            console.warn('API returned error, using demo data');
            // Fallback to demo data if API not ready
            createDemoMolecule();
            return;
        }

        const data = await response.json();
        console.log('Loaded network data:', data);

        // Check if we have any data
        if (!data.projects || data.projects.length === 0) {
            console.warn('No projects found, using demo data');
            createDemoMolecule();
            return;
        }

        buildMolecularStructure(data);
    } catch (error) {
        console.warn('API not available, using demo data:', error);
        createDemoMolecule();
    }
}

function createDemoMolecule() {
    // Create demo molecular structure
    const demoData = {
        projects: [
            { id: 'PROVES', name: 'PROVES', type: 'collaborative', is_nucleus: true },
            { id: 'CubeSat1', name: 'CubeSat Mission 1', type: 'cubesat' },
            { id: 'CubeSat2', name: 'CubeSat Mission 2', type: 'cubesat' },
            { id: 'Research1', name: 'Propulsion Research', type: 'research' }
        ],
        teams: [
            { id: 'T1', name: 'Software Team', project_id: 'CubeSat1' },
            { id: 'T2', name: 'Power Systems', project_id: 'CubeSat1' },
            { id: 'T3', name: 'Structures Team', project_id: 'CubeSat2' },
            { id: 'T4', name: 'Comms Team', project_id: 'PROVES' }
        ],
        faculty: [
            { id: 'F1', name: 'Dr. Smith', role: 'PI' },
            { id: 'F2', name: 'Dr. Lee', role: 'Co-PI' }
        ],
        interfaces: [
            { from: 'PROVES', to: 'CubeSat1', energy_loss: 0.15, type: 'project-project' },
            { from: 'PROVES', to: 'CubeSat2', energy_loss: 0.25, type: 'project-project' },
            { from: 'CubeSat1', to: 'Research1', energy_loss: 0.40, type: 'project-project' },
            { from: 'F1', to: 'PROVES', energy_loss: 0.05, type: 'faculty-project' },
            { from: 'F2', to: 'CubeSat1', energy_loss: 0.10, type: 'faculty-project' },
            { from: 'T1', to: 'CubeSat1', energy_loss: 0.20, type: 'team-project' },
            { from: 'T2', to: 'CubeSat1', energy_loss: 0.30, type: 'team-project' },
            { from: 'T3', to: 'CubeSat2', energy_loss: 0.15, type: 'team-project' },
            { from: 'T4', to: 'PROVES', energy_loss: 0.10, type: 'team-project' },
            { from: 'T1', to: 'T2', energy_loss: 0.25, type: 'team-team' }
        ]
    };

    buildMolecularStructure(demoData);
}

// ============================================================================
// Molecular Structure Builder
// ============================================================================

function buildMolecularStructure(data) {
    // Clear existing
    nodes.forEach(node => scene.remove(node.mesh));
    edges.forEach(edge => {
        scene.remove(edge.line);
        edge.particles.forEach(p => scene.remove(p.mesh));
    });
    nodes.clear();
    edges.clear();
    particles = [];

    // Find nucleus (PROVES)
    const nucleus = data.projects.find(p => p.is_nucleus || p.id === 'PROVES');

    if (nucleus) {
        createNucleus(nucleus);
    }

    // Create orbital layers
    const orbitingProjects = data.projects.filter(p => p.id !== nucleus?.id);
    createProjectOrbits(orbitingProjects, nucleus?.id);

    // Create teams around their projects
    if (data.teams) {
        createTeamNodes(data.teams);
    }

    // Create faculty nodes
    if (data.faculty) {
        createFacultyNodes(data.faculty);
    }

    // Create energy bonds
    if (data.interfaces) {
        createEnergyBonds(data.interfaces);
    }
}

function createNucleus(project) {
    // Large glowing sphere for PROVES at center
    const geometry = new THREE.SphereGeometry(40, 32, 32);
    const material = new THREE.MeshPhongMaterial({
        color: 0x00f0ff,
        emissive: 0x00f0ff,
        emissiveIntensity: 0.5,
        transparent: true,
        opacity: 0.9
    });

    const mesh = new THREE.Mesh(geometry, material);
    mesh.position.set(0, 0, 0);

    // Glow effect
    const glowGeometry = new THREE.SphereGeometry(45, 32, 32);
    const glowMaterial = new THREE.MeshBasicMaterial({
        color: 0x00f0ff,
        transparent: true,
        opacity: 0.2
    });
    const glow = new THREE.Mesh(glowGeometry, glowMaterial);
    mesh.add(glow);

    scene.add(mesh);

    nodes.set(project.id, {
        id: project.id,
        type: 'nucleus',
        data: project,
        mesh: mesh,
        position: new THREE.Vector3(0, 0, 0),
        isNucleus: true
    });
}

function createProjectOrbits(projects, nucleusId) {
    const orbitRadius = 200;
    const angleStep = (Math.PI * 2) / projects.length;

    projects.forEach((project, index) => {
        const angle = angleStep * index;
        const x = Math.cos(angle) * orbitRadius;
        const z = Math.sin(angle) * orbitRadius;
        const y = (Math.random() - 0.5) * 50; // Slight vertical variation

        const geometry = new THREE.SphereGeometry(25, 32, 32);
        const material = new THREE.MeshPhongMaterial({
            color: 0x8b5cf6,
            emissive: 0x8b5cf6,
            emissiveIntensity: 0.3,
            transparent: true,
            opacity: 0.85
        });

        const mesh = new THREE.Mesh(geometry, material);
        mesh.position.set(x, y, z);

        // Orbital ring
        const ringGeometry = new THREE.RingGeometry(orbitRadius - 5, orbitRadius + 5, 64);
        const ringMaterial = new THREE.MeshBasicMaterial({
            color: 0x8b5cf6,
            transparent: true,
            opacity: 0.1,
            side: THREE.DoubleSide
        });
        const ring = new THREE.Mesh(ringGeometry, ringMaterial);
        ring.rotation.x = Math.PI / 2;
        scene.add(ring);

        scene.add(mesh);

        nodes.set(project.id, {
            id: project.id,
            type: 'project',
            data: project,
            mesh: mesh,
            position: new THREE.Vector3(x, y, z),
            orbitAngle: angle,
            orbitRadius: orbitRadius
        });
    });
}

function createTeamNodes(teams) {
    teams.forEach(team => {
        const parentProject = nodes.get(team.project_id);
        if (!parentProject) return;

        // Position near parent project
        const offset = new THREE.Vector3(
            (Math.random() - 0.5) * 80,
            (Math.random() - 0.5) * 80,
            (Math.random() - 0.5) * 80
        );
        const position = parentProject.position.clone().add(offset);

        const geometry = new THREE.SphereGeometry(12, 16, 16);
        const material = new THREE.MeshPhongMaterial({
            color: 0xec4899,
            emissive: 0xec4899,
            emissiveIntensity: 0.2
        });

        const mesh = new THREE.Mesh(geometry, material);
        mesh.position.copy(position);
        scene.add(mesh);

        nodes.set(team.id, {
            id: team.id,
            type: 'team',
            data: team,
            mesh: mesh,
            position: position
        });
    });
}

function createFacultyNodes(faculty) {
    faculty.forEach((person, index) => {
        // Faculty orbit in outer shell
        const orbitRadius = 350;
        const angle = (Math.PI * 2 / faculty.length) * index;
        const x = Math.cos(angle) * orbitRadius;
        const z = Math.sin(angle) * orbitRadius;
        const y = (Math.random() - 0.5) * 100;

        const geometry = new THREE.SphereGeometry(10, 16, 16);
        const material = new THREE.MeshPhongMaterial({
            color: 0xfbbf24,
            emissive: 0xfbbf24,
            emissiveIntensity: 0.3
        });

        const mesh = new THREE.Mesh(geometry, material);
        mesh.position.set(x, y, z);
        scene.add(mesh);

        nodes.set(person.id, {
            id: person.id,
            type: 'faculty',
            data: person,
            mesh: mesh,
            position: new THREE.Vector3(x, y, z)
        });
    });
}

// ============================================================================
// Energy Bonds & Particle Flows
// ============================================================================

function createEnergyBonds(interfaces) {
    interfaces.forEach(bond => {
        const fromNode = nodes.get(bond.from);
        const toNode = nodes.get(bond.to);

        if (!fromNode || !toNode) return;

        // Bond color based on energy loss
        const color = getEnergyColor(bond.energy_loss);

        // Create curved line
        const curve = new THREE.QuadraticBezierCurve3(
            fromNode.position,
            getMidpoint(fromNode.position, toNode.position, bond.energy_loss),
            toNode.position
        );

        const points = curve.getPoints(50);
        const geometry = new THREE.BufferGeometry().setFromPoints(points);
        const material = new THREE.LineBasicMaterial({
            color: color,
            transparent: true,
            opacity: 0.6,
            linewidth: 2
        });

        const line = new THREE.Line(geometry, material);
        scene.add(line);

        // Create particles flowing along bond
        const bondParticles = createParticleFlow(curve, color, bond.energy_loss);

        edges.set(`${bond.from}-${bond.to}`, {
            from: bond.from,
            to: bond.to,
            line: line,
            curve: curve,
            particles: bondParticles,
            energyLoss: bond.energy_loss,
            data: bond
        });
    });
}

function createParticleFlow(curve, color, energyLoss) {
    const particleCount = Math.max(3, Math.floor(10 * (1 - energyLoss)));
    const bondParticles = [];

    for (let i = 0; i < particleCount; i++) {
        const geometry = new THREE.SphereGeometry(2, 8, 8);
        const material = new THREE.MeshBasicMaterial({
            color: color,
            transparent: true,
            opacity: 0.8
        });

        const particle = new THREE.Mesh(geometry, material);
        const point = curve.getPoint(i / particleCount);
        particle.position.copy(point);
        scene.add(particle);

        bondParticles.push({
            mesh: particle,
            curve: curve,
            progress: i / particleCount,
            speed: 0.005 * (1 - energyLoss * 0.5) // Slower flow = more energy loss
        });

        particles.push(bondParticles[bondParticles.length - 1]);
    }

    return bondParticles;
}

function getMidpoint(pos1, pos2, energyLoss) {
    // Higher energy loss = more curvature (unstable bond)
    const mid = new THREE.Vector3().lerpVectors(pos1, pos2, 0.5);
    const curvature = 50 + (energyLoss * 100);
    mid.y += curvature;
    return mid;
}

function getEnergyColor(energyLoss) {
    // Green → Yellow → Orange → Red based on energy loss
    if (energyLoss < 0.15) {
        return new THREE.Color(0x10b981); // Green - healthy
    } else if (energyLoss < 0.35) {
        return new THREE.Color(0xfbbf24); // Yellow - moderate
    } else if (energyLoss < 0.60) {
        return new THREE.Color(0xf59e0b); // Orange - high risk
    } else {
        return new THREE.Color(0xef4444); // Red - critical
    }
}

// ============================================================================
// Animation Loop
// ============================================================================

function animate() {
    animationId = requestAnimationFrame(animate);

    // Update controls
    controls.update();

    // Animate particles along bonds
    particles.forEach(particle => {
        particle.progress += particle.speed;
        if (particle.progress > 1) particle.progress = 0;

        const point = particle.curve.getPoint(particle.progress);
        particle.mesh.position.copy(point);

        // Pulsing effect
        const scale = 1 + Math.sin(Date.now() * 0.005 + particle.progress * Math.PI * 2) * 0.3;
        particle.mesh.scale.set(scale, scale, scale);
    });

    // Orbital rotation for projects
    nodes.forEach(node => {
        if (node.orbitAngle !== undefined && !node.isNucleus) {
            node.orbitAngle += 0.001;
            const x = Math.cos(node.orbitAngle) * node.orbitRadius;
            const z = Math.sin(node.orbitAngle) * node.orbitRadius;
            node.mesh.position.x = x;
            node.mesh.position.z = z;
            node.position.x = x;
            node.position.z = z;
        }
    });

    // Pulsing glow for nucleus
    nodes.forEach(node => {
        if (node.isNucleus) {
            const pulse = 0.5 + Math.sin(Date.now() * 0.001) * 0.2;
            node.mesh.material.emissiveIntensity = pulse;
        }
    });

    renderer.render(scene, camera);
}

// ============================================================================
// Event Listeners & Interaction
// ============================================================================

function setupEventListeners() {
    const canvas = renderer.domElement;

    canvas.addEventListener('click', onCanvasClick);
    canvas.addEventListener('mousemove', onCanvasMouseMove);
}

function onCanvasClick(event) {
    const raycaster = getRaycaster(event);
    const meshes = Array.from(nodes.values()).map(n => n.mesh);
    const intersects = raycaster.intersectObjects(meshes);

    if (intersects.length > 0) {
        const clicked = intersects[0].object;
        const node = Array.from(nodes.values()).find(n => n.mesh === clicked);

        if (node) {
            selectNode(node);
        }
    } else {
        deselectNode();
    }
}

function onCanvasMouseMove(event) {
    const raycaster = getRaycaster(event);
    const meshes = Array.from(nodes.values()).map(n => n.mesh);
    const intersects = raycaster.intersectObjects(meshes);

    if (intersects.length > 0) {
        document.body.style.cursor = 'pointer';
    } else {
        document.body.style.cursor = 'default';
    }
}

function getRaycaster(event) {
    const rect = renderer.domElement.getBoundingClientRect();
    const mouse = new THREE.Vector2();
    mouse.x = ((event.clientX - rect.left) / rect.width) * 2 - 1;
    mouse.y = -((event.clientY - rect.top) / rect.height) * 2 + 1;

    const raycaster = new THREE.Raycaster();
    raycaster.setFromCamera(mouse, camera);
    return raycaster;
}

function selectNode(node) {
    selectedNode = node;

    // Highlight selected node
    node.mesh.material.emissiveIntensity = 0.8;

    // Update info panel
    updateInfoPanel(node);

    // Stop auto-rotation
    controls.autoRotate = false;
}

function deselectNode() {
    if (selectedNode) {
        selectedNode.mesh.material.emissiveIntensity = selectedNode.isNucleus ? 0.5 : 0.3;
        selectedNode = null;
    }

    // Clear info panel
    document.getElementById('nodeDetails').innerHTML = '<p>Click a node to see details.</p>';

    // Resume auto-rotation
    controls.autoRotate = true;
}

function updateInfoPanel(node) {
    const panel = document.getElementById('nodeDetails');

    let html = `<strong>${node.data.name || node.id}</strong><br>`;
    html += `<span style="color:var(--text-secondary)">Type: ${node.type}</span><br>`;

    if (node.type === 'nucleus') {
        html += `<br><span style="color: var(--cyan);">⚛️ Central Project (Nucleus)</span>`;
    }

    // Show connected nodes
    const connections = Array.from(edges.values()).filter(e =>
        e.from === node.id || e.to === node.id
    );

    if (connections.length > 0) {
        html += `<br><br><strong>Connections:</strong> ${connections.length}`;
        html += `<br><small>`;
        connections.slice(0, 5).forEach(conn => {
            const energyPercent = Math.round(conn.energyLoss * 100);
            const color = energyPercent < 15 ? '#10b981' : energyPercent < 35 ? '#fbbf24' : energyPercent < 60 ? '#f59e0b' : '#ef4444';
            html += `<div style="margin: 0.25rem 0; color: ${color};">${energyPercent}% energy loss</div>`;
        });
        html += `</small>`;
    }

    panel.innerHTML = html;
}

// Cleanup on page unload
window.addEventListener('beforeunload', () => {
    if (animationId) {
        cancelAnimationFrame(animationId);
    }

    if (renderer) {
        renderer.dispose();
    }
});
