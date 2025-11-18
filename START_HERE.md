# 🚀 FRAMES - Quick Start Guide

## What You Have Now

Your HTML application has been converted to a Flask + JavaScript architecture:

```
✅ Python Backend (Flask)
✅ REST API (All CRUD operations)
✅ Analytics Engine (NDA diagnostics in Python)
✅ Data Persistence (Saved to JSON file)
✅ API Client (JavaScript communication layer)
✅ Test Page (Verify everything works)
✅ Original HTML (Preserved for reference)
```

## Step 1: Install Dependencies

Open PowerShell or Command Prompt:

```powershell
cd "c:\Users\LizO5\FRAMES Python"
pip install -r requirements.txt
```

This installs:
- Flask (web framework)
- Flask-CORS (allows frontend-backend communication)

## Step 2: Start the Backend Server

```powershell
cd backend
python app.py
```

You should see:
```
Starting FRAMES Flask application...
Access the application at: http://localhost:5000
 * Running on http://0.0.0.0:5000
```

**Keep this terminal window open!** The server must stay running.

## Step 3: Test the Application

Open your browser and go to:
```
http://localhost:5000
```

You should see a test page with buttons. Try these in order:

1. **Test Backend Connection** - Should show ✅ success
2. **Load Sample Data** - Loads Bronco Space Lab data
3. **Get Teams** - Should show 8 teams
4. **Get Statistics** - Should show system metrics
5. **Get NDA Diagnostic** - Should show analysis

## Step 4: Check the API

Open browser DevTools (F12) → Console tab

Try these commands:

```javascript
// Load sample data
await FramesAPI.loadSampleData();

// Get all teams
const teams = await FramesAPI.getTeams();
console.log(teams);

// Get analytics
const stats = await FramesAPI.getStatistics();
console.log(stats);

// Get NDA diagnostic
const nda = await FramesAPI.getNDADiagnostic();
console.log(nda);
```

## Step 5: Verify Data Persistence

1. Load sample data (if not already loaded)
2. Stop the Flask server (Ctrl+C in terminal)
3. Restart the server: `python app.py`
4. Refresh browser and click "Get Teams"
5. **Data should still be there!** (saved in `frames_data.json`)

## What Works Right Now

✅ **Backend API**
- Create/Read/Delete teams, faculty, projects, interfaces
- All analytics functions (NDA diagnostic, backward tracing, etc.)
- Data persistence to JSON file
- Load sample data

✅ **Frontend API Client**
- JavaScript functions to call all backend endpoints
- Async/await pattern for clean code

## What You Need to Do Next

### Priority 1: Migrate Your Full HTML

Your original 2423-line HTML file is saved as:
```
frontend/templates/index_original.html
```

**Read the MIGRATION_GUIDE.md** for step-by-step instructions on:
1. Copying the full HTML structure
2. Copying all CSS styles
3. Modifying JavaScript functions to use `FramesAPI`
4. Testing each function as you migrate

### Priority 2: Add Drag-and-Drop

For your inverse mapping feature (visual → data), you'll need to:
1. Choose a library: **Cytoscape.js** (recommended) or D3.js
2. Implement drag handlers
3. Calculate inverse relationships from positions
4. Update backend via API

## File Structure

```
FRAMES Python/
├── backend/
│   ├── app.py              ← Flask server & API
│   ├── models.py           ← Data classes
│   ├── analytics.py        ← NDA diagnostics
│   └── frames_data.json    ← Your data (auto-created)
├── frontend/
│   ├── templates/
│   │   ├── index.html      ← Test page (current)
│   │   └── index_original.html  ← Your full HTML
│   └── static/
│       └── api.js          ← API client
├── requirements.txt        ← Python dependencies
├── README.md              ← Full documentation
├── MIGRATION_GUIDE.md     ← Step-by-step migration
└── START_HERE.md          ← This file
```

## Common Issues

### ❌ "pip: command not found"
Python is not in your PATH. Try:
```powershell
python -m pip install -r requirements.txt
```

### ❌ "Address already in use"
Port 5000 is taken. Change port in `backend/app.py`:
```python
app.run(debug=True, host='0.0.0.0', port=5001)
```

### ❌ "Failed to connect to backend"
Make sure Flask is running:
```powershell
cd backend
python app.py
```

### ❌ "CORS error"
Make sure Flask-CORS is installed:
```powershell
pip install Flask-CORS
```

## Next Steps

1. ✅ **[DONE]** Test backend API
2. 📝 **[TODO]** Read `MIGRATION_GUIDE.md`
3. 📝 **[TODO]** Migrate your full HTML
4. 📝 **[TODO]** Add drag-and-drop library
5. 📝 **[TODO]** Implement inverse mapping

## Questions?

Check these files:
- **README.md** - Full documentation
- **MIGRATION_GUIDE.md** - How to migrate HTML
- **api.js** - All available API functions

## Success Checklist

- [ ] Flask server starts without errors
- [ ] Test page loads at http://localhost:5000
- [ ] "Test Backend Connection" button works
- [ ] "Load Sample Data" button works
- [ ] "Get Teams" shows 8 teams
- [ ] Data persists after server restart
- [ ] Ready to migrate full HTML

---

**You're all set!** The backend is complete and working. Now you just need to migrate your HTML/JavaScript to use the new API. See `MIGRATION_GUIDE.md` for details.
