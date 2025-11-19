// dashboard.js - Proof of concept for dynamic network dashboard
// Uses vis-network for interactive graph

document.addEventListener('DOMContentLoaded', function () {
    // Mock data: nodes and edges
    const nodes = new vis.DataSet([
        { id: 1, label: 'Dr. Jane Smith', group: 'faculty', title: 'Faculty Advisor' },
        { id: 2, label: 'Software Team', group: 'team', title: 'Team' },
        { id: 3, label: 'CubeSat Mission', group: 'project', title: 'Project' },
        { id: 4, label: 'John Doe', group: 'student', title: 'Student' },
        { id: 5, label: 'Dr. Alan Lee', group: 'faculty', title: 'Faculty Advisor' },
        { id: 6, label: 'Power Systems Team', group: 'team', title: 'Team' },
        { id: 7, label: 'Mary Johnson', group: 'student', title: 'Student' },
    ]);

    const edges = new vis.DataSet([
        { from: 1, to: 2, label: 'advises' },
        { from: 2, to: 3, label: 'works on' },
        { from: 4, to: 2, label: 'member' },
        { from: 5, to: 6, label: 'advises' },
        { from: 6, to: 3, label: 'works on' },
        { from: 7, to: 6, label: 'member' },
        { from: 1, to: 3, label: 'PI' },
    ]);

    // Network options
    const options = {
        nodes: {
            shape: 'dot',
            size: 20,
            font: {
                face: 'Space Grotesk',
                color: '#00f0ff',
                size: 16,
                bold: true
            },
            borderWidth: 2
        },
        groups: {
            faculty: { color: { background: '#0d1117', border: '#00f0ff' }, font: { color: '#00f0ff' } },
            team: { color: { background: '#8b5cf6', border: '#00f0ff' }, font: { color: '#fff' } },
            project: { color: { background: '#22223b', border: '#8b5cf6' }, font: { color: '#8b5cf6' } },
            student: { color: { background: '#00f0ff', border: '#8b5cf6' }, font: { color: '#0a0a0f' } }
        },
        edges: {
            color: '#7d8590',
            font: { color: '#7d8590', size: 12, face: 'Inter' },
            arrows: 'to',
            smooth: {
                type: 'cubicBezier',
                forceDirection: 'horizontal',
                roundness: 0.4
            }
        },
        layout: {
            improvedLayout: true
        },
        physics: {
            stabilization: true,
            barnesHut: {
                gravitationalConstant: -30000,
                springLength: 200
            }
        },
        interaction: {
            hover: true,
            tooltipDelay: 100,
            navigationButtons: true,
            selectable: true
        }
    };

    const container = document.getElementById('network');
    const data = { nodes, edges };
    const network = new vis.Network(container, data, options);

    // Info panel update
    network.on('selectNode', function (params) {
        const node = nodes.get(params.nodes[0]);
        document.getElementById('nodeDetails').innerHTML = `
            <strong>${node.label}</strong><br>
            <span style="color:var(--text-secondary)">${node.title}</span><br>
            <span style="font-size:0.95em;">Type: ${node.group.charAt(0).toUpperCase() + node.group.slice(1)}</span>
        `;
    });
    network.on('deselectNode', function () {
        document.getElementById('nodeDetails').innerHTML = '<p>Select a node to see details.</p>';
    });
});
