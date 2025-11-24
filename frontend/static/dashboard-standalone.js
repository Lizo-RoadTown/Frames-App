/**
 * FRAMES 3D Molecular Knowledge Network Visualization (Standalone)
 *
 * Architecture:
 * - PROVES (nucleus) at center
 * - Major projects orbit around PROVES
 * - Teams, faculty, students connect between projects
 * - Animated particle flows show knowledge transfer energy
 * - Color-coded bonds: green (healthy) → yellow → orange → red (critical)
 *
 * Uses global THREE from CDN for PythonAnywhere compatibility
 */

// API configuration
const API_BASE_URL = `${window.location.origin}/api`;

// Global state
let scene, camera, renderer, controls;
let nodes = new Map();
let edges = new Map();
let particles = [];
let selectedNode = null;
let isDragging = false;
let draggedNode = null;
let universityId = null;
let isResearcher = false; // Will be set based on user role

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
    console.log('Dashboard initializing...');
    console.log('THREE available:', typeof THREE !== 'undefined');
    console.log('OrbitControls available:', typeof OrbitControls !== 'undefined');
    console.log('THREE.OrbitControls available:', typeof THREE !== 'undefined' && typeof THREE.OrbitControls !== 'undefined');

    // Get university from URL
    const urlParams = new URLSearchParams(window.location.search);
    universityId = urlParams.get('university');
    isResearcher = urlParams.get('researcher') === 'true'; // Check if user is a researcher
    console.log('University ID:', universityId);
    console.log('Is Researcher:', isResearcher);

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
        console.error('Error stack:', error.stack);
        document.getElementById('nodeDetails').innerHTML = `
            <p style="color: #ef4444;">Error loading 3D visualization</p>
            <p style="font-size: 0.875rem;">${error.message}</p>
            <p style="font-size: 0.875rem;">Check browser console for details.</p>
        `;
    }
});

function initScene() {
    // Check if OrbitControls is available
    if (typeof OrbitControls === 'undefined' && typeof THREE !== 'undefined' && THREE.OrbitControls) {
        window.OrbitControls = THREE.OrbitControls;
    }
    
    if (typeof OrbitControls === 'undefined') {
        throw new Error('OrbitControls is not defined. Check that Three.js scripts are loaded correctly.');
    }

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

    // Controls (using global OrbitControls from CDN)
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

    // Create student nodes (micro-modules within teams)
    if (data.students) {
        createStudentNodes(data.students);
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
    // Group teams by project to evenly distribute them
    const teamsByProject = new Map();
    teams.forEach(team => {
        if (!teamsByProject.has(team.project_id)) {
            teamsByProject.set(team.project_id, []);
        }
        teamsByProject.get(team.project_id).push(team);
    });

    teams.forEach(team => {
        const parentProject = nodes.get(team.project_id);
        if (!parentProject) return;

        // Get index of this team within their project
        const projectTeams = teamsByProject.get(team.project_id);
        const teamIndexInProject = projectTeams.indexOf(team);
        const teamsInProject = projectTeams.length;

        // Teams orbit around their parent project (like moons around planets)
        const teamOrbitRadius = 60; // Orbit radius around project
        const angleStep = (Math.PI * 2) / teamsInProject;
        const angle = angleStep * teamIndexInProject;

        const x = parentProject.position.x + Math.cos(angle) * teamOrbitRadius;
        const z = parentProject.position.z + Math.sin(angle) * teamOrbitRadius;
        const y = parentProject.position.y + (Math.sin(angle) * 10); // Slight vertical variation

        const position = new THREE.Vector3(x, y, z);

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
            position: position,
            orbitAngle: angle,
            orbitRadius: teamOrbitRadius,
            parentProjectId: team.project_id // Store parent project ID for dynamic orbit updates
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

function createStudentNodes(students) {
    // Group students by team to evenly distribute them
    const studentsByTeam = new Map();
    students.forEach(student => {
        if (!studentsByTeam.has(student.team_id)) {
            studentsByTeam.set(student.team_id, []);
        }
        studentsByTeam.get(student.team_id).push(student);
    });

    students.forEach((student) => {
        const parentTeam = nodes.get(student.team_id);
        if (!parentTeam) {
            console.warn(`Parent team ${student.team_id} not found for student ${student.id}`);
            return;
        }

        // Get index of this student within their team
        const teamStudents = studentsByTeam.get(student.team_id);
        const studentIndexInTeam = teamStudents.indexOf(student);
        const studentsInTeam = teamStudents.length;

        // Students orbit within their team sphere (like electrons)
        // Evenly distribute students around the team
        const teamOrbitRadius = 20; // Small radius around team
        const angleStep = (Math.PI * 2) / studentsInTeam;
        const angle = angleStep * studentIndexInTeam;

        const x = parentTeam.position.x + Math.cos(angle) * teamOrbitRadius;
        const z = parentTeam.position.z + Math.sin(angle) * teamOrbitRadius;
        const y = parentTeam.position.y + (Math.sin(angle * 2) * 5); // Slight vertical variation

        const position = new THREE.Vector3(x, y, z);

        // Color code by status: incoming (orange), established (green), outgoing (red)
        let color, emissiveColor;
        if (student.status === 'incoming') {
            color = 0xf59e0b; // Orange
            emissiveColor = 0xf59e0b;
        } else if (student.status === 'outgoing') {
            color = 0xef4444; // Red
            emissiveColor = 0xef4444;
        } else {
            color = 0x10b981; // Green (established)
            emissiveColor = 0x10b981;
        }

        const geometry = new THREE.SphereGeometry(5, 12, 12);
        const material = new THREE.MeshPhongMaterial({
            color: color,
            emissive: emissiveColor,
            emissiveIntensity: 0.4,
            transparent: true,
            opacity: 0.9
        });

        const mesh = new THREE.Mesh(geometry, material);
        mesh.position.copy(position);
        scene.add(mesh);

        nodes.set(student.id, {
            id: student.id,
            type: 'student',
            data: student,
            mesh: mesh,
            position: position,
            orbitAngle: angle,
            orbitRadius: teamOrbitRadius,
            parentTeamId: student.team_id // Store parent team ID for dynamic orbit updates
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

        // Bond thickness based on strength (inverse of energy loss)
        // Strong bonds (low energy loss) = thick, Weak bonds (high energy loss) = thin
        const bondStrength = 1 - bond.energy_loss;
        const tubeRadius = 0.5 + (bondStrength * 2.5); // Range: 0.5 to 3.0

        // Create tube geometry for visible thickness
        const tubeGeometry = new THREE.TubeGeometry(curve, 20, tubeRadius, 8, false);
        const tubeMaterial = new THREE.MeshBasicMaterial({
            color: color,
            transparent: true,
            opacity: 0.4
        });

        const tube = new THREE.Mesh(tubeGeometry, tubeMaterial);
        scene.add(tube);

        // Create particles flowing along bond
        const bondParticles = createParticleFlow(curve, color, bond.energy_loss);

        edges.set(`${bond.from}-${bond.to}`, {
            from: bond.from,
            to: bond.to,
            line: tube,
            curve: curve,
            particles: bondParticles,
            energyLoss: bond.energy_loss,
            bondStrength: bondStrength,
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

    // Orbital rotation for projects, teams, and students
    nodes.forEach(node => {
        if (node.orbitAngle !== undefined && !node.isNucleus) {
            if (node.type === 'student' && node.parentTeamId) {
                // Students orbit around their team center (faster rotation like electrons)
                const parentTeam = nodes.get(node.parentTeamId);
                if (parentTeam) {
                    node.orbitAngle += 0.005; // Faster rotation for students
                    const x = parentTeam.position.x + Math.cos(node.orbitAngle) * node.orbitRadius;
                    const z = parentTeam.position.z + Math.sin(node.orbitAngle) * node.orbitRadius;
                    const y = parentTeam.position.y + (Math.sin(node.orbitAngle * 2) * 5); // Slight bobbing
                    node.mesh.position.x = x;
                    node.mesh.position.y = y;
                    node.mesh.position.z = z;
                    node.position.x = x;
                    node.position.y = y;
                    node.position.z = z;
                }
            } else if (node.type === 'project') {
                // Projects orbit around nucleus (slower)
                node.orbitAngle += 0.001;
                const x = Math.cos(node.orbitAngle) * node.orbitRadius;
                const z = Math.sin(node.orbitAngle) * node.orbitRadius;
                node.mesh.position.x = x;
                node.mesh.position.z = z;
                node.position.x = x;
                node.position.z = z;
            } else if (node.type === 'team' && node.parentProjectId) {
                // Teams orbit around their parent project (medium speed)
                const parentProject = nodes.get(node.parentProjectId);
                if (parentProject) {
                    node.orbitAngle += 0.003;
                    const x = parentProject.position.x + Math.cos(node.orbitAngle) * node.orbitRadius;
                    const z = parentProject.position.z + Math.sin(node.orbitAngle) * node.orbitRadius;
                    const y = parentProject.position.y + (Math.sin(node.orbitAngle) * 10);
                    node.mesh.position.x = x;
                    node.mesh.position.y = y;
                    node.mesh.position.z = z;
                    node.position.x = x;
                    node.position.y = y;
                    node.position.z = z;
                }
            }
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
            document.body.style.cursor = 'grab';
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
                console.log('Permission denied: Cannot drag this node');
                // Show visual feedback that drag is not allowed
                showPermissionDenied(node);
                return;
            }

            isDragging = true;
            draggedNode = node;
            document.body.style.cursor = 'grabbing';

            // Set up the drag plane oriented to face the camera
            dragPlane.position.copy(node.mesh.position);
            dragPlane.lookAt(camera.position);

            // Calculate offset between mouse ray and object position
            const planeIntersects = raycaster.intersectObject(dragPlane);
            if (planeIntersects.length > 0) {
                dragOffset.copy(node.mesh.position).sub(planeIntersects[0].point);
            }

            // Stop auto-rotation while dragging
            controls.autoRotate = false;
        }
    }
}

function canDragNode(node) {
    // Researchers can drag everything
    if (isResearcher) {
        return true;
    }

    // For single university view: users can only drag nodes from their own university
    // In this dashboard, all nodes belong to the selected university
    // So if universityId matches, user can drag
    return universityId !== null;
}

function showPermissionDenied(node) {
    // Flash the node red briefly to show permission denied
    const originalColor = node.mesh.material.color.clone();
    node.mesh.material.color.setHex(0xff0000);

    setTimeout(() => {
        node.mesh.material.color.copy(originalColor);
    }, 200);

    // Update info panel
    const panel = document.getElementById('nodeDetails');
    panel.innerHTML = `
        <p style="color: #ef4444; font-weight: 600;">⚠️ Permission Denied</p>
        <p style="font-size: 0.875rem; margin-top: 0.5rem;">
            You can only edit your own university's network.
        </p>
        <p style="font-size: 0.875rem; margin-top: 0.5rem;">
            Click to view details only.
        </p>
    `;
}

function onMouseUp(event) {
    if (isDragging && draggedNode) {
        isDragging = false;
        controls.enabled = true;

        // If it was a quick click (not much dragging), select the node
        selectNode(draggedNode);

        draggedNode = null;
        document.body.style.cursor = 'default';
    }
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
                const tubeRadius = 0.5 + (bondStrength * 2.5);
                const color = getEnergyColor(edge.energyLoss);

                // Remove old tube
                scene.remove(edge.line);

                // Create new tube
                const tubeGeometry = new THREE.TubeGeometry(newCurve, 20, tubeRadius, 8, false);
                const tubeMaterial = new THREE.MeshBasicMaterial({
                    color: color,
                    transparent: true,
                    opacity: 0.4
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

    // Add type-specific info
    if (node.type === 'nucleus') {
        html += `<br><span style="color: var(--cyan);">⚛️ Central Project (Nucleus)</span>`;
    } else if (node.type === 'student') {
        const statusColors = {
            'incoming': '#f59e0b',
            'established': '#10b981',
            'outgoing': '#ef4444'
        };
        const statusColor = statusColors[node.data.status] || '#64ffda';
        html += `<br><span style="color: ${statusColor};">Status: ${node.data.status}</span>`;
        if (node.data.year) {
            html += `<br><span style="color:var(--text-secondary)">Year: ${node.data.year}</span>`;
        }
    } else if (node.type === 'team') {
        if (node.data.lifecycle) {
            html += `<br><span style="color:var(--text-secondary)">Lifecycle: ${node.data.lifecycle}</span>`;
        }
        if (node.data.discipline) {
            html += `<br><span style="color:var(--text-secondary)">Discipline: ${node.data.discipline}</span>`;
        }
    } else if (node.type === 'faculty') {
        if (node.data.role) {
            html += `<br><span style="color:var(--text-secondary)">${node.data.role}</span>`;
        }
    }

    // Show connected nodes with bond strength details
    const connections = Array.from(edges.values()).filter(e =>
        e.from === node.id || e.to === node.id
    );

    if (connections.length > 0) {
        html += `<br><br><strong>Bonds:</strong> ${connections.length} total`;
        html += `<br><div style="font-size: 0.75rem; max-height: 200px; overflow-y: auto;">`;

        connections.slice(0, 10).forEach(conn => {
            const energyPercent = Math.round(conn.energyLoss * 100);
            const strengthPercent = Math.round(conn.bondStrength * 100);
            const color = energyPercent < 15 ? '#10b981' : energyPercent < 35 ? '#fbbf24' : energyPercent < 60 ? '#f59e0b' : '#ef4444';

            // Get the other node's name
            const otherId = conn.from === node.id ? conn.to : conn.from;
            const otherNode = nodes.get(otherId);
            const otherName = otherNode ? (otherNode.data.name || otherId) : otherId;

            // Bond strength indicator (thickness visualization)
            const thicknessBar = '█'.repeat(Math.max(1, Math.floor(strengthPercent / 20)));

            html += `<div style="margin: 0.5rem 0; padding: 0.25rem; background: rgba(255,255,255,0.05); border-left: 3px solid ${color};">`;
            html += `<div style="font-weight: 600;">${otherName}</div>`;
            html += `<div style="color: ${color};">Energy Loss: ${energyPercent}%</div>`;
            html += `<div style="color: #64ffda;">Bond Strength: ${strengthPercent}% <span style="letter-spacing: -2px;">${thicknessBar}</span></div>`;
            html += `<div style="color:var(--text-secondary); font-size: 0.7rem;">${conn.data.type || 'interface'}</div>`;
            html += `</div>`;
        });

        if (connections.length > 10) {
            html += `<div style="color:var(--text-secondary); margin-top: 0.5rem; font-style: italic;">...and ${connections.length - 10} more</div>`;
        }

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

// ============================================================================
// Sample Data Loading (for testing without backend)
// ============================================================================

window.loadComprehensiveSampleData = function() {
    console.log('Loading comprehensive sample data with students...');

    const comprehensiveData = {
        projects: [
            { id: 'PROVES', name: 'PROVES', type: 'collaborative', is_nucleus: true },
            { id: 'JPL_CubeSat', name: 'JPL CubeSat Mission', type: 'contract' },
            { id: 'Multi_Uni', name: 'Multi-University Research', type: 'collaborative' },
            { id: 'Contract_Pursuit', name: 'Contract Proposal', type: 'proposal' }
        ],
        teams: [
            // PROVES teams
            { id: 'proves_core', name: 'PROVES Core Team', project_id: 'PROVES', discipline: 'Multidisciplinary', lifecycle: 'established' },

            // JPL CubeSat teams
            { id: 'power_sys', name: 'Power Systems', project_id: 'JPL_CubeSat', discipline: 'Electrical', lifecycle: 'established' },
            { id: 'flight_sw', name: 'Flight Software', project_id: 'JPL_CubeSat', discipline: 'Software', lifecycle: 'established' },
            { id: 'comms', name: 'Communications', project_id: 'JPL_CubeSat', discipline: 'Electrical', lifecycle: 'incoming' },

            // Multi-University teams
            { id: 'mission_ops', name: 'Mission Operations', project_id: 'Multi_Uni', discipline: 'Mission Ops', lifecycle: 'established' },
            { id: 'mechanical', name: 'Mechanical Systems', project_id: 'Multi_Uni', discipline: 'Mechanical', lifecycle: 'established' },

            // Contract Pursuit teams
            { id: 'proposal_eng', name: 'Proposal Engineering', project_id: 'Contract_Pursuit', discipline: 'Engineering', lifecycle: 'incoming' },
            { id: 'legacy_sw', name: 'Software Legacy', project_id: 'Contract_Pursuit', discipline: 'Software', lifecycle: 'outgoing' }
        ],
        students: [
            // PROVES Core Team students
            { id: 's1', name: 'Alice Chen', team_id: 'proves_core', status: 'established', year: 3 },
            { id: 's2', name: 'Bob Martinez', team_id: 'proves_core', status: 'established', year: 3 },
            { id: 's3', name: 'Carol Kim', team_id: 'proves_core', status: 'established', year: 4 },

            // Power Systems students
            { id: 's4', name: 'David Lopez', team_id: 'power_sys', status: 'established', year: 3 },
            { id: 's5', name: 'Emma Wilson', team_id: 'power_sys', status: 'established', year: 4 },
            { id: 's6', name: 'Frank Zhang', team_id: 'power_sys', status: 'incoming', year: 2 },
            { id: 's7', name: 'Grace Lee', team_id: 'power_sys', status: 'established', year: 3 },

            // Flight Software students
            { id: 's8', name: 'Henry Patel', team_id: 'flight_sw', status: 'established', year: 4 },
            { id: 's9', name: 'Iris Johnson', team_id: 'flight_sw', status: 'established', year: 3 },
            { id: 's10', name: 'Jack Brown', team_id: 'flight_sw', status: 'incoming', year: 2 },
            { id: 's11', name: 'Kelly Davis', team_id: 'flight_sw', status: 'established', year: 3 },
            { id: 's12', name: 'Leo Garcia', team_id: 'flight_sw', status: 'established', year: 4 },

            // Communications students
            { id: 's13', name: 'Maya Singh', team_id: 'comms', status: 'incoming', year: 2 },
            { id: 's14', name: 'Noah Taylor', team_id: 'comms', status: 'incoming', year: 2 },
            { id: 's15', name: 'Olivia White', team_id: 'comms', status: 'incoming', year: 1 },

            // Mission Ops students
            { id: 's16', name: 'Peter Anderson', team_id: 'mission_ops', status: 'established', year: 3 },
            { id: 's17', name: 'Quinn Thomas', team_id: 'mission_ops', status: 'established', year: 4 },
            { id: 's18', name: 'Rachel Moore', team_id: 'mission_ops', status: 'incoming', year: 2 },
            { id: 's19', name: 'Sam Jackson', team_id: 'mission_ops', status: 'established', year: 3 },

            // Mechanical Systems students
            { id: 's20', name: 'Tina Martin', team_id: 'mechanical', status: 'established', year: 4 },
            { id: 's21', name: 'Uma Patel', team_id: 'mechanical', status: 'established', year: 3 },
            { id: 's22', name: 'Victor Lee', team_id: 'mechanical', status: 'incoming', year: 2 },

            // Proposal Engineering students
            { id: 's23', name: 'Wendy Clark', team_id: 'proposal_eng', status: 'incoming', year: 1 },
            { id: 's24', name: 'Xavier Rodriguez', team_id: 'proposal_eng', status: 'incoming', year: 2 },

            // Legacy Software students (outgoing)
            { id: 's25', name: 'Yuki Tanaka', team_id: 'legacy_sw', status: 'outgoing', year: 4 },
            { id: 's26', name: 'Zoe Williams', team_id: 'legacy_sw', status: 'outgoing', year: 4 }
        ],
        faculty: [
            { id: 'f1', name: 'Dr. Sarah Chen', role: 'Principal Investigator' },
            { id: 'f2', name: 'Dr. James Rodriguez', role: 'Technical Lead' },
            { id: 'f3', name: 'Dr. Maria Garcia', role: 'Program Director' }
        ],
        interfaces: [
            // PROVES to other projects (nucleus connections) - healthy
            { from: 'PROVES', to: 'JPL_CubeSat', energy_loss: 0.10, type: 'knowledge_transfer' },
            { from: 'PROVES', to: 'Multi_Uni', energy_loss: 0.12, type: 'knowledge_transfer' },
            { from: 'PROVES', to: 'Contract_Pursuit', energy_loss: 0.15, type: 'knowledge_transfer' },

            // Project to Team connections
            { from: 'PROVES', to: 'proves_core', energy_loss: 0.08, type: 'project_team' },
            { from: 'JPL_CubeSat', to: 'power_sys', energy_loss: 0.12, type: 'project_team' },
            { from: 'JPL_CubeSat', to: 'flight_sw', energy_loss: 0.10, type: 'project_team' },
            { from: 'JPL_CubeSat', to: 'comms', energy_loss: 0.25, type: 'project_team' },
            { from: 'Multi_Uni', to: 'mission_ops', energy_loss: 0.15, type: 'project_team' },
            { from: 'Multi_Uni', to: 'mechanical', energy_loss: 0.18, type: 'project_team' },
            { from: 'Contract_Pursuit', to: 'proposal_eng', energy_loss: 0.40, type: 'project_team' },
            { from: 'Contract_Pursuit', to: 'legacy_sw', energy_loss: 0.65, type: 'project_team' },

            // Team to Student connections (showing varying bond strengths)
            { from: 'proves_core', to: 's1', energy_loss: 0.05, type: 'team_student' },
            { from: 'proves_core', to: 's2', energy_loss: 0.08, type: 'team_student' },
            { from: 'proves_core', to: 's3', energy_loss: 0.10, type: 'team_student' },

            { from: 'power_sys', to: 's4', energy_loss: 0.12, type: 'team_student' },
            { from: 'power_sys', to: 's5', energy_loss: 0.10, type: 'team_student' },
            { from: 'power_sys', to: 's6', energy_loss: 0.30, type: 'team_student' }, // Incoming student
            { from: 'power_sys', to: 's7', energy_loss: 0.15, type: 'team_student' },

            { from: 'flight_sw', to: 's8', energy_loss: 0.08, type: 'team_student' },
            { from: 'flight_sw', to: 's9', energy_loss: 0.12, type: 'team_student' },
            { from: 'flight_sw', to: 's10', energy_loss: 0.35, type: 'team_student' }, // Incoming
            { from: 'flight_sw', to: 's11', energy_loss: 0.14, type: 'team_student' },
            { from: 'flight_sw', to: 's12', energy_loss: 0.10, type: 'team_student' },

            { from: 'comms', to: 's13', energy_loss: 0.40, type: 'team_student' }, // New team
            { from: 'comms', to: 's14', energy_loss: 0.38, type: 'team_student' },
            { from: 'comms', to: 's15', energy_loss: 0.50, type: 'team_student' },

            { from: 'mission_ops', to: 's16', energy_loss: 0.15, type: 'team_student' },
            { from: 'mission_ops', to: 's17', energy_loss: 0.12, type: 'team_student' },
            { from: 'mission_ops', to: 's18', energy_loss: 0.28, type: 'team_student' },
            { from: 'mission_ops', to: 's19', energy_loss: 0.18, type: 'team_student' },

            { from: 'mechanical', to: 's20', energy_loss: 0.14, type: 'team_student' },
            { from: 'mechanical', to: 's21', energy_loss: 0.16, type: 'team_student' },
            { from: 'mechanical', to: 's22', energy_loss: 0.32, type: 'team_student' },

            { from: 'proposal_eng', to: 's23', energy_loss: 0.55, type: 'team_student' }, // Very new
            { from: 'proposal_eng', to: 's24', energy_loss: 0.45, type: 'team_student' },

            { from: 'legacy_sw', to: 's25', energy_loss: 0.70, type: 'team_student' }, // Graduating
            { from: 'legacy_sw', to: 's26', energy_loss: 0.68, type: 'team_student' },

            // Faculty mentoring connections
            { from: 'f1', to: 'proves_core', energy_loss: 0.10, type: 'mentoring' },
            { from: 'f1', to: 'JPL_CubeSat', energy_loss: 0.12, type: 'mentoring' },
            { from: 'f2', to: 'flight_sw', energy_loss: 0.15, type: 'mentoring' },
            { from: 'f2', to: 'power_sys', energy_loss: 0.18, type: 'mentoring' },
            { from: 'f3', to: 'mission_ops', energy_loss: 0.20, type: 'mentoring' },
            { from: 'f3', to: 'mechanical', energy_loss: 0.22, type: 'mentoring' },

            // Cross-team knowledge transfer
            { from: 'power_sys', to: 'flight_sw', energy_loss: 0.20, type: 'team_team' },
            { from: 'flight_sw', to: 'comms', energy_loss: 0.30, type: 'team_team' },
            { from: 'legacy_sw', to: 'flight_sw', energy_loss: 0.50, type: 'team_team' }, // Knowledge loss from graduating team

            // Student to student collaboration (within and across teams)
            { from: 's8', to: 's9', energy_loss: 0.08, type: 'student_student' }, // Same team, strong
            { from: 's4', to: 's8', energy_loss: 0.25, type: 'student_student' }, // Cross-team
            { from: 's25', to: 's12', energy_loss: 0.60, type: 'student_student' }  // Outgoing to established
        ]
    };

    // Rebuild the visualization with this data
    buildMolecularStructure(comprehensiveData);

    // Update info panel
    document.getElementById('nodeDetails').innerHTML = `
        <p style="color: #10b981; font-weight: 600;">✓ Sample data loaded!</p>
        <p style="font-size: 0.875rem; margin-top: 10px;">
            <strong>4</strong> projects<br>
            <strong>8</strong> teams<br>
            <strong>26</strong> students<br>
            <strong>3</strong> faculty<br>
            <strong>60+</strong> interfaces
        </p>
        <p style="font-size: 0.75rem; color: var(--text-secondary); margin-top: 10px;">
            Click any node to see details
        </p>
    `;

    console.log('Sample data loaded successfully');
};
