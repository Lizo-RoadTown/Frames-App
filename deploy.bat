@echo off
REM Deployment script for FRAMES app to PythonAnywhere
REM Run this script after making changes to deploy updates

echo ========================================
echo FRAMES Deployment Script
echo ========================================
echo.

REM Check if there are changes to commit
git status

echo.
echo ========================================
echo Step 1: Commit your changes
echo ========================================
echo.

set /p commit_message="Enter commit message (or press Enter to skip commit): "

if not "%commit_message%"=="" (
    echo Committing changes...
    git add .
    git commit -m "%commit_message%"
    echo.
    echo ✓ Changes committed
) else (
    echo Skipping commit step
)

echo.
echo ========================================
echo Step 2: Push to GitHub
echo ========================================
echo.

git push
if %errorlevel% neq 0 (
    echo ✗ Failed to push to GitHub
    pause
    exit /b 1
)

echo ✓ Pushed to GitHub successfully!
echo.

echo ========================================
echo Step 3: Update PythonAnywhere
echo ========================================
echo.
echo Now you need to update PythonAnywhere:
echo.
echo 1. Go to: https://www.pythonanywhere.com
echo 2. Open a Bash console
echo 3. Run these commands:
echo.
echo    cd Frames-App
echo    git pull
echo.
echo 4. Go to the Web tab
echo 5. Click the green "Reload" button
echo.
echo ========================================
echo Your app will be live at:
echo https://eosborn.pythonanywhere.com
echo ========================================
echo.

pause
