@echo off
echo Starting Budget Tracker Application...
echo.

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Check if migrations need to be run
echo Checking for pending migrations...
python manage.py makemigrations --check --dry-run > nul 2>&1
if errorlevel 1 (
    echo Running migrations...
    python manage.py makemigrations
    python manage.py migrate
)

REM Start the development server
echo.
echo Starting Django development server...
echo Dashboard will be available at: http://127.0.0.1:8000/
echo Admin panel will be available at: http://127.0.0.1:8000/admin/
echo.
echo Default admin credentials:
echo Username: admin
echo Password: admin123
echo.
echo Press Ctrl+C to stop the server
echo.
python manage.py runserver
