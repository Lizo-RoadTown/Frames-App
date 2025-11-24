# Migration Guide: HTML to Flask + JavaScript

This guide explains how your original `index.html` has been converted to a Flask + JavaScript architecture.

## What Was Done

### 1. Backend Created (Python/Flask)
- **models.py** - Your teams, faculty, projects, interfaces are now Python classes
- **analytics.py** - All diagnostic functions ported to Python
- **app.py** - REST API endpoints for all operations

### 2. Frontend Separated
- **HTML** → `frontend/templates/index.html`
- **CSS** → Kept inline in HTML (can extract to `frontend/static/style.css` later)
- **JavaScript** → Split into:
  - `frontend/static/api.js` - Backend communication
  - Your original JS → Stays in HTML (will modify to use API)

### 3. API Layer Added
JavaScript now communicates with Python backend via REST API instead of storing data locally.

## How to Complete the Migration

Your original `index.html` (2423 lines) has been copied to:
```
frontend/templates/index_original.html
```

### Step 1: Extract CSS (Optional but Recommended)

Extract the `<style>` section (lines 6-478) to `frontend/static/style.css`

Then in HTML, replace the `<style>` block with:
```html
<link rel="stylesheet" href="/static/style.css">
```

### Step 2: Modify JavaScript to Use API

The key changes needed in your JavaScript:

#### Old Way (Local Arrays):
```javascript
let teams = [];
let faculty = [];
// ...

function addTeam() {
    const team = { /* ... */ };
    teams.push(team);  // Local storage
    updateTeamList();
}
```

#### New Way (API Calls):
```javascript
async function addTeam() {
    const team = { /* ... */ };
    const created = await FramesAPI.createTeam(team);  // Save to backend
    await loadData();  // Reload from backend
    updateTeamList();
}
```

### Step 3: Load Data on Page Load

Add this at the top of your `<script>` section:

```javascript
let teams = [];
let faculty = [];
let projects = [];
let interfaces = [];

// Load data from backend when page loads
async function loadData() {
    const state = await FramesAPI.getState();
    teams = state.teams;
    faculty = state.faculty;
    projects = state.projects;
    interfaces = state.interfaces;

    updateTeamList();
    updateFacultyList();
    updateProjectList();
    updateInterfaceList();
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', async function() {
    await loadData();
    // ... rest of your initialization code
});
```

### Step 4: Update All Mutation Functions

Find and replace these patterns:

#### Add Functions
```javascript
// OLD
teams.push(team);

// NEW
await FramesAPI.createTeam(team);
await loadData();
```

#### Remove Functions
```javascript
// OLD
teams = teams.filter(t => t.id !== teamId);

// NEW
await FramesAPI.deleteTeam(teamId);
await loadData();
```

#### Update Functions
```javascript
// NEW - if you add update functionality
await FramesAPI.updateTeam(teamId, updatedTeamData);
await loadData();
```

## Quick Start Testing

### 1. Start Backend
```bash
cd backend
python app.py
```

### 2. Load Sample Data
Open browser to `http://localhost:5000` and run in console:
```javascript
await FramesAPI.loadSampleData();
await loadData();
```

### 3. Test API
```javascript
// Get all teams
const teams = await FramesAPI.getTeams();
console.log(teams);

// Get statistics
const stats = await FramesAPI.getStatistics();
console.log(stats);

// Get NDA diagnostics
const nda = await FramesAPI.getNDADiagnostic();
console.log(nda);
```

## Files You Need to Modify

### Priority 1 (Essential):
1. **`frontend/templates/index.html`** - Your main HTML file
   - Add `<script src="/static/api.js"></script>` in the `<head>`
   - Modify JavaScript functions to use `FramesAPI`
   - Add `loadData()` function
   - Update all CRUD operations

### Priority 2 (Recommended):
2. **Extract CSS** to `frontend/static/style.css`
3. **Extract JavaScript** to `frontend/static/app.js`

### Priority 3 (Future Enhancement):
4. **Add drag-and-drop library** (Cytoscape.js recommended)
5. **Implement inverse mapping logic**
6. **Add WebSocket support** for real-time collaboration

## Example: Converting addTeam()

### Before (Original HTML):
```javascript
function addTeam() {
    const discipline = document.getElementById('teamDiscipline').value;
    const lifecycle = document.getElementById('teamLifecycle').value;
    const name = document.getElementById('teamName').value.trim();
    const size = parseInt(document.getElementById('teamSize').value);
    const experience = parseInt(document.getElementById('teamExperience').value);
    const description = document.getElementById('teamDescription').value.trim();

    if (!name) {
        alert('Please enter a team name/identifier');
        return;
    }

    const team = {
        id: 'team_' + Date.now(),
        discipline: discipline,
        lifecycle: lifecycle,
        name: name,
        size: size,
        experience: experience,
        description: description
    };

    teams.push(team);  // <-- LOCAL STORAGE
    updateTeamList();
    updateInterfaceTargets();

    // Clear form...
}
```

### After (Flask + API):
```javascript
async function addTeam() {
    const discipline = document.getElementById('teamDiscipline').value;
    const lifecycle = document.getElementById('teamLifecycle').value;
    const name = document.getElementById('teamName').value.trim();
    const size = parseInt(document.getElementById('teamSize').value);
    const experience = parseInt(document.getElementById('teamExperience').value);
    const description = document.getElementById('teamDescription').value.trim();

    if (!name) {
        alert('Please enter a team name/identifier');
        return;
    }

    const team = {
        discipline: discipline,
        lifecycle: lifecycle,
        name: name,
        size: size,
        experience: experience,
        description: description
    };

    try {
        await FramesAPI.createTeam(team);  // <-- SAVE TO BACKEND
        await loadData();  // <-- RELOAD FROM BACKEND
        updateTeamList();
        updateInterfaceTargets();

        // Clear form...
    } catch (error) {
        console.error('Error adding team:', error);
        alert('Failed to add team. See console for details.');
    }
}
```

## Testing Strategy

1. **Test Backend First**
   ```bash
   cd backend
   python app.py
   ```
   Visit `http://localhost:5000/api/teams` - should return `[]`

2. **Test API Client**
   Open browser console and test:
   ```javascript
   await FramesAPI.loadSampleData();
   const teams = await FramesAPI.getTeams();
   console.log(teams);  // Should show 8 teams
   ```

3. **Test Each Function**
   - Test adding a team
   - Test removing a team
   - Test adding interfaces
   - Test visualization

## Need Help?

If you get stuck during migration:
1. Check browser console for errors
2. Check Flask server console for errors
3. Test API endpoints directly using browser or Postman
4. Compare with original HTML to see what changed

## Next Steps After Migration

Once the basic migration is complete:
1. **Add Drag-and-Drop** - Use Cytoscape.js or D3.js
2. **Implement Inverse Mapping** - Calculate data from visual positions
3. **Add Undo/Redo** - Use backend state management
4. **Add Export/Import** - Download/upload JSON
5. **Add User Authentication** - Multi-user support
6. **Add Database** - Replace JSON file with PostgreSQL/MongoDB
