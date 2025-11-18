# FRAMES Deployment Guide

Your FRAMES app is deployed at: **https://eosborn.pythonanywhere.com**

GitHub Repository: **https://github.com/Lizo-RoadTown/Frames-App**

---

## Quick Deploy (After Making Changes)

### Option 1: Using the Script (Easiest)

Just double-click `deploy.bat` and follow the prompts!

### Option 2: Manual Steps

**On your computer:**
```bash
git add .
git commit -m "Description of your changes"
git push
```

**On PythonAnywhere:**
1. Go to https://www.pythonanywhere.com
2. Click "Consoles" → Open your Bash console
3. Run:
   ```bash
   cd Frames-App
   git pull
   ```
4. Go to "Web" tab
5. Click the green "Reload" button

---

## Important URLs

- **Live App**: https://eosborn.pythonanywhere.com
- **GitHub Repo**: https://github.com/Lizo-RoadTown/Frames-App
- **PythonAnywhere Dashboard**: https://www.pythonanywhere.com/user/eosborn/

---

## Common Tasks

### Update the App
1. Make changes locally
2. Run `deploy.bat`
3. Follow the prompts
4. Update on PythonAnywhere (instructions in script output)

### View Error Logs
1. Go to PythonAnywhere → Web tab
2. Scroll to "Log files" section
3. Click on the error log

### Reset Database
On PythonAnywhere bash console:
```bash
cd Frames-App/backend
rm frames.db
python -c "from app import app, db; app.app_context().push(); db.create_all()"
```

Then reload the web app.

---

## What Universities See

When universities visit https://eosborn.pythonanywhere.com, they'll see:
- The FRAMES application interface
- Ability to load sample data
- All the visualization and analysis features
- Their changes persist in the database

---

## Free Tier Limits

PythonAnywhere free tier includes:
- ✅ One web app (you're using it)
- ✅ Always-on (doesn't sleep)
- ✅ SQLite database with persistence
- ✅ Enough for demos and university testing
- ⚠️ App sleeps after inactivity (wakes up automatically when visited)

---

## Need Help?

If something breaks:
1. Check the error logs on PythonAnywhere (Web tab → Log files)
2. Try reloading the web app
3. Check if changes were pushed to GitHub
4. Verify you ran `git pull` on PythonAnywhere

---

## Docker Note

You asked about Docker earlier - **you don't need it!**

PythonAnywhere handles all the containerization and hosting for you. Just push to GitHub and pull on PythonAnywhere. Much simpler than Docker for your use case.
