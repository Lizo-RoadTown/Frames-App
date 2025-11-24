/**
 * FRAMES Multi-University Network Visualization
 *
 * Architecture:
 * - Cal Poly Pomona (nucleus) at center - the "sun"
 * - All 7 other universities orbit around Cal Poly Pomona
 * - Each university shows their project/team connections
 * - PROVES collaboration connects all universities
 */

// API configuration
const API_BASE_URL = `${window.location.origin}/api`;

// Global state
let scene, camera, renderer, controls;
let nodes = new Map();
let edges = new Map();
let particles = [];
let selectedNode = null;
let universityId = null;
let isResearcher = false; // Will be set based on user role
let isDragging = false;
let draggedNode = null;

// Animation
let animationId = null;

// Drag state
let dragPlane = null;
let dragOffset = new THREE.Vector3();
let dragIntersection = new THREE.Vector3();

// ============================================================================
// Initialization
// ============================================================================

window.addEventListener('DOMContentLoaded', async () => {
    console.log('Multi-University Network initializing...');

    // Check if user is a researcher
    const urlParams = new URLSearchParams(window.location.search);
    isResearcher = urlParams.get('researcher') === 'true';
    universityId = urlParams.get('university'); // Optional: for regular users viewing from their dashboard
    console.log('Is Researcher:', isResearcher);
    console.log('University ID:', universityId);

    try {
        initScene();
        console.log('Scene initialized');

        // Auto-load the network on page load
        await loadMultiUniversityData();
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
    scene.fog = new THREE.Fog(0x0a0a0f, 500, 3000);

    // Camera
    const container = document.getElementById('network');
    camera = new THREE.PerspectiveCamera(
        60,
        container.clientWidth / container.clientHeight,
        1,
        5000
    );
    camera.position.set(0, 500, 1000);
    camera.lookAt(0, 0, 0);

    // Renderer
    renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
    renderer.setSize(container.clientWidth, container.clientHeight);
    renderer.setPixelRatio(window.devicePixelRatio);
    container.appendChild(renderer.domElement);

    // Controls
    controls = new THREE.OrbitControls(camera, renderer.domElement);
    controls.enableDamping = true;
    controls.dampingFactor = 0.05;
    controls.minDistance = 300;
    controls.maxDistance = 2000;
    controls.autoRotate = true;
    controls.autoRotateSpeed = 0.3;

    // Lights
    const ambientLight = new THREE.AmbientLight(0x404040, 1.5);
    scene.add(ambientLight);

    const pointLight1 = new THREE.PointLight(0x00f0ff, 2, 1500);
    pointLight1.position.set(300, 300, 300);
    scene.add(pointLight1);

    const pointLight2 = new THREE.PointLight(0x8b5cf6, 1.5, 1500);
    pointLight2.position.set(-300, -300, 300);
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

window.loadMultiUniversityData = function() {
    console.log('Loading multi-university network data...');

    const multiUniversityData = {
        universities: [
            { id: 'CalPolyPomona', name: 'Cal Poly Pomona', location: 'Pomona, CA', role: 'Lead Institution', isNucleus: true },
            { id: 'TexasState', name: 'Texas State University', location: 'San Marcos, TX', role: 'Partner' },
            { id: 'Columbia', name: 'Columbia University', location: 'New York, NY', role: 'Partner' },
            { id: 'UniversityD', name: 'University D', location: 'TBD', role: 'Partner' },
            { id: 'UniversityE', name: 'University E', location: 'TBD', role: 'Partner' },
            { id: 'UniversityF', name: 'University F', location: 'TBD', role: 'Partner' },
            { id: 'UniversityG', name: 'University G', location: 'TBD', role: 'Partner' },
            { id: 'UniversityH', name: 'University H', location: 'TBD', role: 'Partner' }
        ],
        collaborations: [
            // PROVES connections - all universities connect to Cal Poly
            { from: 'CalPolyPomona', to: 'TexasState', energy_loss: 0.12, type: 'PROVES collaboration', strength: 'strong' },
            { from: 'CalPolyPomona', to: 'Columbia', energy_loss: 0.15, type: 'PROVES collaboration', strength: 'strong' },
            { from: 'CalPolyPomona', to: 'UniversityD', energy_loss: 0.25, type: 'PROVES collaboration', strength: 'moderate' },
            { from: 'CalPolyPomona', to: 'UniversityE', energy_loss: 0.20, type: 'PROVES collaboration', strength: 'moderate' },
            { from: 'CalPolyPomona', to: 'UniversityF', energy_loss: 0.30, type: 'PROVES collaboration', strength: 'developing' },
            { from: 'CalPolyPomona', to: 'UniversityG', energy_loss: 0.28, type: 'PROVES collaboration', strength: 'developing' },
            { from: 'CalPolyPomona', to: 'UniversityH', energy_loss: 0.35, type: 'PROVES collaboration', strength: 'developing' },

            // Direct university-to-university collaborations
            { from: 'TexasState', to: 'Columbia', energy_loss: 0.40, type: 'cross-university', strength: 'emerging' },
            { from: 'Columbia', to: 'UniversityD', energy_loss: 0.45, type: 'cross-university', strength: 'emerging' },
            { from: 'UniversityE', to: 'UniversityF', energy_loss: 0.50, type: 'cross-university', strength: 'nascent' }
        ]
    };

    buildMultiUniversityNetwork(multiUniversityData);

    // Update info panel
    document.getElementById('nodeDetails').innerHTML = `
        <p style="color: #10b981; font-weight: 600;">✓ Multi-University Network loaded!</p>
        <p style="font-size: 0.875rem; margin-top: 10px;">
            <strong>8</strong> universities<br>
            <strong>10</strong> collaborations<br>
            <strong>Cal Poly Pomona</strong> at center
        </p>
        <p style="font-size: 0.75rem; color: var(--text-secondary); margin-top: 10px;">
            Click any university to see details
        </p>
    `;

    console.log('Multi-university network loaded successfully');
};

// ============================================================================
// Network Builder
// ============================================================================

function buildMultiUniversityNetwork(data) {
    // Clear existing
    nodes.forEach(node => scene.remove(node.mesh));
    edges.forEach(edge => {
        scene.remove(edge.line);
        edge.particles.forEach(p => scene.remove(p.mesh));
    });
    nodes.clear();
    edges.clear();
    particles = [];

    // Find nucleus (Cal Poly Pomona - the "sun")
    const nucleus = data.universities.find(u => u.isNucleus);

    if (nucleus) {
        createUniversityNucleus(nucleus);
    }

    // Create orbiting universities
    const orbitingUniversities = data.universities.filter(u => !u.isNucleus);
    createOrbitingUniversities(orbitingUniversities);

    // Create collaboration bonds
    if (data.collaborations) {
        createCollaborationBonds(data.collaborations);
    }
}

function createUniversityNucleus(university) {
    // Large glowing sphere for Cal Poly Pomona at center (the "sun")
    const geometry = new THREE.SphereGeometry(60, 32, 32);
    const material = new THREE.MeshPhongMaterial({
        color: 0xffd700, // Gold for the lead institution
        emissive: 0xffd700,
        emissiveIntensity: 0.6,
        transparent: true,
        opacity: 0.95
    });

    const mesh = new THREE.Mesh(geometry, material);
    mesh.position.set(0, 0, 0);

    // Glow effect
    const glowGeometry = new THREE.SphereGeometry(70, 32, 32);
    const glowMaterial = new THREE.MeshBasicMaterial({
        color: 0xffd700,
        transparent: true,
        opacity: 0.2
    });
    const glow = new THREE.Mesh(glowGeometry, glowMaterial);
    mesh.add(glow);

    scene.add(mesh);

    nodes.set(university.id, {
        id: university.id,
        type: 'nucleus',
        data: university,
        mesh: mesh,
        position: new THREE.Vector3(0, 0, 0),
        isNucleus: true
    });
}

function createOrbitingUniversities(universities) {
    const orbitRadius = 400;
    const angleStep = (Math.PI * 2) / universities.length;

    universities.forEach((university, index) => {
        const angle = angleStep * index;
        const x = Math.cos(angle) * orbitRadius;
        const z = Math.sin(angle) * orbitRadius;
        const y = (Math.random() - 0.5) * 80; // Slight vertical variation

        const geometry = new THREE.SphereGeometry(35, 32, 32);
        const material = new THREE.MeshPhongMaterial({
            color: 0x00f0ff,
            emissive: 0x00f0ff,
            emissiveIntensity: 0.4,
            transparent: true,
            opacity: 0.9
        });

        const mesh = new THREE.Mesh(geometry, material);
        mesh.position.set(x, y, z);

        scene.add(mesh);

        nodes.set(university.id, {
            id: university.id,
            type: 'university',
            data: university,
            mesh: mesh,
            position: new THREE.Vector3(x, y, z),
            orbitAngle: angle,
            orbitRadius: orbitRadius
        });
    });
}

// ============================================================================
// Collaboration Bonds
// ============================================================================

function createCollaborationBonds(collaborations) {
    collaborations.forEach(collab => {
        const fromNode = nodes.get(collab.from);
        const toNode = nodes.get(collab.to);

        if (!fromNode || !toNode) return;

        // Bond color based on energy loss
        const color = getEnergyColor(collab.energy_loss);

        // Create curved line
        const curve = new THREE.QuadraticBezierCurve3(
            fromNode.position,
            getMidpoint(fromNode.position, toNode.position, collab.energy_loss),
            toNode.position
        );

        // Bond thickness based on strength
        const bondStrength = 1 - collab.energy_loss;
        const tubeRadius = 1.0 + (bondStrength * 4.0); // Range: 1.0 to 5.0 (thicker for universities)

        // Create tube geometry
        const tubeGeometry = new THREE.TubeGeometry(curve, 20, tubeRadius, 8, false);
        const tubeMaterial = new THREE.MeshBasicMaterial({
            color: color,
            transparent: true,
            opacity: 0.5
        });

        const tube = new THREE.Mesh(tubeGeometry, tubeMaterial);
        scene.add(tube);

        // Create particles flowing along bond
        const bondParticles = createParticleFlow(curve, color, collab.energy_loss);

        edges.set(`${collab.from}-${collab.to}`, {
            from: collab.from,
            to: collab.to,
            line: tube,
            curve: curve,
            particles: bondParticles,
            energyLoss: collab.energy_loss,
            bondStrength: bondStrength,
            data: collab
        });
    });
}

function createParticleFlow(curve, color, energyLoss) {
    const particleCount = Math.max(3, Math.floor(10 * (1 - energyLoss)));
    const bondParticles = [];

    for (let i = 0; i < particleCount; i++) {
        const geometry = new THREE.SphereGeometry(3, 8, 8);
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
            speed: 0.003 * (1 - energyLoss * 0.5)
        });

        particles.push(bondParticles[bondParticles.length - 1]);
    }

    return bondParticles;
}

function getMidpoint(pos1, pos2, energyLoss) {
    const mid = new THREE.Vector3().lerpVectors(pos1, pos2, 0.5);
    const curvature = 60 + (energyLoss * 120);
    mid.y += curvature;
    return mid;
}

function getEnergyColor(energyLoss) {
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

    // Orbital rotation for universities
    nodes.forEach(node => {
        if (node.orbitAngle !== undefined && !node.isNucleus) {
            node.orbitAngle += 0.0005; // Slow rotation around Cal Poly
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
            const pulse = 0.6 + Math.sin(Date.now() * 0.001) * 0.2;
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
    canvas.addEventListener('mousedown', onMouseDown);
    canvas.addEventListener('mouseup', onMouseUp);

    // Create an invisible drag plane for 3D dragging
    const planeGeometry = new THREE.PlaneGeometry(5000, 5000);
    const planeMaterial = new THREE.MeshBasicMaterial({ visible: false });
    dragPlane = new THREE.Mesh(planeGeometry, planeMaterial);
    scene.add(dragPlane);
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
    if (isDragging && draggedNode) {
        // Dragging mode: move the node
        const raycaster = getRaycaster(event);
        const intersects = raycaster.intersectObject(dragPlane);

        if (intersects.length > 0) {
            const intersectPoint = intersects[0].point;
            draggedNode.mesh.position.copy(intersectPoint.add(dragOffset));
            draggedNode.position.copy(draggedNode.mesh.position);

            // Update connected edges
            updateConnectedEdges(draggedNode);

            // Disable orbit controls while dragging
            controls.enabled = false;
        }
    } else {
        // Hover mode: show cursor feedback
        const raycaster = getRaycaster(event);
        const meshes = Array.from(nodes.values()).map(n => n.mesh);
        const intersects = raycaster.intersectObjects(meshes);

        if (intersects.length > 0) {
            const node = Array.from(nodes.values()).find(n => n.mesh === intersects[0].object);
            // Show grab cursor only if user can drag this node
            if (node && canDragNode(node)) {
                document.body.style.cursor = 'grab';
            } else {
                document.body.style.cursor = 'pointer';
            }
        } else {
            document.body.style.cursor = 'default';
        }
    }
}

function onMouseDown(event) {
    const raycaster = getRaycaster(event);
    const meshes = Array.from(nodes.values()).map(n => n.mesh);
    const intersects = raycaster.intersectObjects(meshes);

    if (intersects.length > 0) {
        const clicked = intersects[0].object;
        const node = Array.from(nodes.values()).find(n => n.mesh === clicked);

        if (node) {
            // Permission check: Can this node be dragged?
            if (!canDragNode(node)) {
                console.log('Permission denied: Cannot drag this university');
                showPermissionDenied(node);
                return;
            }

            isDragging = true;
            draggedNode = node;
            document.body.style.cursor = 'grabbing';

            // Set up the drag plane
            dragPlane.position.copy(node.mesh.position);
            dragPlane.lookAt(camera.position);

            // Calculate offset
            const planeIntersects = raycaster.intersectObject(dragPlane);
            if (planeIntersects.length > 0) {
                dragOffset.copy(node.mesh.position).sub(planeIntersects[0].point);
            }

            // Stop auto-rotation
            controls.autoRotate = false;
        }
    }
}

function onMouseUp(event) {
    if (isDragging && draggedNode) {
        isDragging = false;
        controls.enabled = true;

        // Select the node
        selectNode(draggedNode);

        draggedNode = null;
        document.body.style.cursor = 'default';
    }
}

function canDragNode(node) {
    // Researchers can drag ANY university
    if (isResearcher) {
        return true;
    }

    // Regular users cannot drag universities in the multi-university view
    // (They can only drag in their own single-university dashboard)
    return false;
}

function showPermissionDenied(node) {
    // Flash the node red briefly
    const originalColor = node.mesh.material.color.clone();
    node.mesh.material.color.setHex(0xff0000);

    setTimeout(() => {
        node.mesh.material.color.copy(originalColor);
    }, 200);

    // Update info panel
    const panel = document.getElementById('nodeDetails');
    panel.innerHTML = `
        <p style="color: #ef4444; font-weight: 600;">⚠️ Researcher Access Only</p>
        <p style="font-size: 0.875rem; margin-top: 0.5rem;">
            Only researchers can edit the multi-university network.
        </p>
        <p style="font-size: 0.875rem; margin-top: 0.5rem;">
            Use your individual university dashboard to edit your own network.
        </p>
    `;
}

function updateConnectedEdges(node) {
    // Rebuild curves for all connected edges
    edges.forEach((edge, key) => {
        if (edge.from === node.id || edge.to === node.id) {
            const fromNode = nodes.get(edge.from);
            const toNode = nodes.get(edge.to);

            if (fromNode && toNode) {
                // Update the curve
                const newCurve = new THREE.QuadraticBezierCurve3(
                    fromNode.position,
                    getMidpoint(fromNode.position, toNode.position, edge.energyLoss),
                    toNode.position
                );

                // Update tube geometry
                const bondStrength = 1 - edge.energyLoss;
                const tubeRadius = 1.0 + (bondStrength * 4.0);
                const color = getEnergyColor(edge.energyLoss);

                // Remove old tube
                scene.remove(edge.line);

                // Create new tube
                const tubeGeometry = new THREE.TubeGeometry(newCurve, 20, tubeRadius, 8, false);
                const tubeMaterial = new THREE.MeshBasicMaterial({
                    color: color,
                    transparent: true,
                    opacity: 0.5
                });
                const newTube = new THREE.Mesh(tubeGeometry, tubeMaterial);
                scene.add(newTube);

                // Update edge data
                edge.curve = newCurve;
                edge.line = newTube;
            }
        }
    });
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
    node.mesh.material.emissiveIntensity = 0.9;

    // Update info panel
    updateInfoPanel(node);

    // Stop auto-rotation
    controls.autoRotate = false;
}

function deselectNode() {
    if (selectedNode) {
        selectedNode.mesh.material.emissiveIntensity = selectedNode.isNucleus ? 0.6 : 0.4;
        selectedNode = null;
    }

    // Clear info panel
    document.getElementById('nodeDetails').innerHTML = '<p>Click a university to see details.</p>';

    // Resume auto-rotation
    controls.autoRotate = true;
}

function updateInfoPanel(node) {
    const panel = document.getElementById('nodeDetails');

    let html = `<strong style="font-size: 1.2rem;">${node.data.name}</strong><br>`;
    html += `<span style="color:var(--text-secondary)">${node.data.location}</span><br>`;

    if (node.type === 'nucleus') {
        html += `<br><span style="color: #ffd700;">☀️ Lead Institution</span>`;
        html += `<br><p style="margin-top: 0.5rem; font-size: 0.875rem;">All universities orbit around Cal Poly Pomona, representing the coordinated multi-university collaboration.</p>`;
    } else {
        html += `<br><span style="color:var(--text-secondary)">${node.data.role}</span>`;
    }

    // Show collaborations
    const connections = Array.from(edges.values()).filter(e =>
        e.from === node.id || e.to === node.id
    );

    if (connections.length > 0) {
        html += `<br><br><strong>Collaborations:</strong> ${connections.length}`;
        html += `<br><div style="font-size: 0.75rem; max-height: 200px; overflow-y: auto;">`;

        connections.forEach(conn => {
            const energyPercent = Math.round(conn.energyLoss * 100);
            const strengthPercent = Math.round(conn.bondStrength * 100);
            const color = energyPercent < 15 ? '#10b981' : energyPercent < 35 ? '#fbbf24' : energyPercent < 60 ? '#f59e0b' : '#ef4444';

            const otherId = conn.from === node.id ? conn.to : conn.from;
            const otherNode = nodes.get(otherId);
            const otherName = otherNode ? otherNode.data.name : otherId;

            const thicknessBar = '█'.repeat(Math.max(1, Math.floor(strengthPercent / 20)));

            html += `<div style="margin: 0.5rem 0; padding: 0.25rem; background: rgba(255,255,255,0.05); border-left: 3px solid ${color};">`;
            html += `<div style="font-weight: 600;">${otherName}</div>`;
            html += `<div style="color: ${color};">Energy Loss: ${energyPercent}%</div>`;
            html += `<div style="color: #64ffda;">Strength: ${strengthPercent}% <span style="letter-spacing: -2px;">${thicknessBar}</span></div>`;
            html += `<div style="color:var(--text-secondary); font-size: 0.7rem;">${conn.data.type}</div>`;
            html += `</div>`;
        });

        html += `</div>`;
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
