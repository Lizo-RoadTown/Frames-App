# Windows Development Setup Guide

## Your Environment
- **OS**: Windows 11 with WSL available (but not required)
- **Python**: 3.14
- **Project Location**: `C:\Users\LizO5\FRAMES Python`
- **Virtual Environment**: Windows-native venv at `backend/venv`

## Quick Start (PowerShell or Command Prompt)

### Activate Virtual Environment
```powershell
cd "C:\Users\LizO5\FRAMES Python\backend"
venv\Scripts\activate
```

### Run Flask App
```powershell
cd "C:\Users\LizO5\FRAMES Python\backend"
venv\Scripts\activate
python app.py
```
The app will be available at: http://localhost:5000

### Deactivate Virtual Environment
```powershell
deactivate
```

## Common Tasks

### Install New Package
```powershell
cd "C:\Users\LizO5\FRAMES Python"
backend\venv\Scripts\pip.exe install package-name
```

### Update Requirements File
```powershell
cd "C:\Users\LizO5\FRAMES Python"
backend\venv\Scripts\pip.exe freeze > requirements.txt
```

### Load Sample Data
From PowerShell:
```powershell
cd "C:\Users\LizO5\FRAMES Python"
backend\venv\Scripts\python.exe test_sample_data.py
```

Or manually with SQL script:
```powershell
cd "C:\Users\LizO5\FRAMES Python"
python manual_load_sample_data.py
```

### Verify Database
```powershell
cd "C:\Users\LizO5\FRAMES Python"
python scripts\verify_migration.py
```

## Troubleshooting

### "Module not found" Error
Make sure you're using the venv Python:
```powershell
backend\venv\Scripts\python.exe your_script.py
```

### Cannot Run Scripts in PowerShell
If you get execution policy errors:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Recreate Virtual Environment
```powershell
cd "C:\Users\LizO5\FRAMES Python\backend"
rmdir /s /q venv
python -m venv venv
venv\Scripts\pip.exe install -r ..\requirements.txt
```

## File Structure
```
C:\Users\LizO5\FRAMES Python\
├── backend/
│   ├── venv/                    # Windows virtual environment
│   ├── app.py                   # Flask application
│   ├── models.py                # Data models
│   ├── db_models.py             # SQLAlchemy models
│   ├── analytics.py             # Analytics functions
│   └── frames.db                # SQLite database
├── frontend/
│   ├── static/                  # CSS, JS files
│   └── templates/               # HTML templates
├── scripts/
│   └── verify_migration.py      # Database verification script
├── requirements.txt             # Python dependencies
├── test_sample_data.py          # Test script for /api/sample-data
└── manual_load_sample_data.py  # Direct SQL data loader

## Notes
- You do NOT need WSL for this project
- All commands work in PowerShell, Command Prompt, or Git Bash
- VSCode works perfectly with Windows paths
- The venv is now Windows-native (no broken symlinks)
```
