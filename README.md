# FRAMES - Python/Flask Version

Framework for Resilience Assessment in Modular Engineering Systems

This is the Python/Flask conversion of the original HTML-based FRAMES application, enabling:
- Real-time data persistence
- Backend analytics processing
- RESTful API for future enhancements
- Preparation for drag-and-drop inverse mapping (visual → data)

## Architecture Briefing

The full architecture briefing for FRAMES (v2) is in `feature-requests/FRAMES_System_Architecture_Briefing_v2.md`.
Read that document before making large architectural changes.

## Project Structure

```
FRAMES Python/
├── backend/
│   ├── app.py              # Flask application & API endpoints
│   ├── models.py           # Data models (Team, Faculty, Project, Interface)
│   └── analytics.py        # NDA diagnostics & analytics functions
├── frontend/
│   ├── templates/
│   │   └── index.html      # Main application page
│   └── static/
│       ├── api.js          # API client for backend communication
│       ├── app.js          # Main application logic
│       └── style.css       # Styling
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

## Installation

### 1. Install Python Dependencies

```bash
cd "c:\Users\LizO5\FRAMES Python"
pip install -r requirements.txt
```

### 2. Run the Flask Server

```bash
cd backend
python app.py
```

The server will start on `http://localhost:5000`

### 3. Access the Application

Open your browser and navigate to:
```
http://localhost:5000
```

## Features

### Current (Migrated from HTML version)

- ✅ Create and manage Teams, Faculty, and Projects
- ✅ Define interfaces between entities
- ✅ Visualize molecular structure with energy flow
- ✅ NDA diagnostic analysis
- ✅ Backward tracing analysis
- ✅ Team lifecycle analysis
- ✅ Data persistence (saved to `frames_data.json`)

### Coming Soon (Your Requirements)

- 🔄 **Drag-and-drop nodes** - Move molecules visually
- 🔄 **Inverse mapping** - Update data based on visual changes
- 🔄 **Real-time collaboration** - Multiple users editing simultaneously
- 🔄 **Advanced analytics** - More diagnostic dimensions
- 🔄 **Export/Import** - Save and load system configurations

## API Endpoints

### Teams
- `GET /api/teams` - Get all teams
- `POST /api/teams` - Create a new team
- `PUT /api/teams/<id>` - Update a team
- `DELETE /api/teams/<id>` - Delete a team

### Faculty
- `GET /api/faculty` - Get all faculty
- `POST /api/faculty` - Create new faculty
- `DELETE /api/faculty/<id>` - Delete faculty

### Projects
- `GET /api/projects` - Get all projects
- `POST /api/projects` - Create new project
- `DELETE /api/projects/<id>` - Delete project

### Interfaces
- `GET /api/interfaces` - Get all interfaces
- `POST /api/interfaces` - Create new interface
- `DELETE /api/interfaces/<id>` - Delete interface

### Analytics
- `GET /api/analytics/statistics` - Get system statistics
- `GET /api/analytics/nda-diagnostic` - Get NDA diagnostic analysis
- `GET /api/analytics/backward-tracing` - Get backward tracing analysis
- `GET /api/analytics/team-lifecycle` - Get team lifecycle analysis

### System State
- `GET /api/state` - Get complete system state
- `POST /api/state` - Set complete system state
- `POST /api/state/reset` - Reset to empty state
- `POST /api/sample-data` - Load Bronco Space Lab sample data

## Next Steps for Inverse Mapping

To implement drag-and-drop with inverse mapping (visual → data):

### 1. Add Drag-and-Drop Library
Consider using:
- **Cytoscape.js** - Graph visualization with built-in drag support
- **D3.js + D3-Force** - Physics-based graph layout
- **Konva.js** - Canvas-based drag-and-drop

### 2. Capture Node Position Changes
```javascript
// Pseudo-code example
node.on('dragend', function(event) {
    const newPosition = { x: event.x, y: event.y };

    // Calculate what data changes would produce this position
    const updatedRelationships = calculateInverseMapping(newPosition);

    // Update backend
    await FramesAPI.updateMoleculeRelationships(updatedRelationships);
});
```

### 3. Implement Inverse Calculation
The inverse mapping logic will:
- Detect new distances between nodes
- Calculate implied interface strengths
- Suggest bond type changes based on proximity
- Update team lifecycle based on position relative to projects

## Development Notes

### Data Persistence
Data is automatically saved to `frames_data.json` after each change. This file is created in the `backend/` directory.

### CORS Enabled
The Flask app has CORS enabled to allow frontend-backend communication during development.

### Debug Mode
The Flask app runs in debug mode by default for easier development. Disable in production:
```python
app.run(debug=False, host='0.0.0.0', port=5000)
```

## Architecture Benefits

### Backend (Python/Flask)
- **Data validation** - Ensure data integrity
- **Complex analytics** - NDA diagnostics run server-side
- **Persistence** - Automatic state saving
- **Scalability** - Can add database (PostgreSQL, MongoDB)
- **API** - Can integrate with other tools

### Frontend (HTML/CSS/JS)
- **Interactivity** - Real-time visualization updates
- **Animations** - Energy particles, bond flickering
- **Drag-and-drop** - Direct manipulation interface
- **Responsive** - Works on different screen sizes

### Separation of Concerns
- Frontend handles visualization and user interaction
- Backend handles data management and analytics
- Clean API contract between them

## Troubleshooting

### Port Already in Use
If port 5000 is in use, change the port in `backend/app.py`:
```python
app.run(debug=True, host='0.0.0.0', port=5001)  # Use 5001 instead
```

### CORS Errors
If you see CORS errors in the browser console, ensure Flask-CORS is installed:
```bash
pip install Flask-CORS
```

### Data Not Persisting
Check that the `backend/` directory is writable. The app creates `frames_data.json` automatically.

## Contact

For questions about the FRAMES system, refer to the original Bronco Space Lab documentation.
