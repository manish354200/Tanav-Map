@echo off
REM Quick Start Script for Mental Health Monitoring System (Windows)

echo.
echo 🚀 Mental Health Monitoring System - Quick Start
echo ==================================================
echo.

REM Check if Docker is installed
docker --version >nul 2>&1
if errorlevel 1 (
    echo Docker not found. Please install Docker Desktop for Windows.
    exit /b 1
)

echo ✓ Docker found
echo.

REM Get the project directory
set PROJECT_DIR=%cd%

echo Project Directory: %PROJECT_DIR%
echo.

REM Create environment files if they don't exist
echo Setting up environment files...

if not exist "%PROJECT_DIR%\backend\.env" (
    copy "%PROJECT_DIR%\backend\.env.example" "%PROJECT_DIR%\backend\.env"
    echo ✓ Created backend\.env
)

if not exist "%PROJECT_DIR%\frontend\.env" (
    copy "%PROJECT_DIR%\frontend\.env.example" "%PROJECT_DIR%\frontend\.env"
    echo ✓ Created frontend\.env
)

echo.

REM Build and start Docker services
echo Starting Docker services...
echo (This may take a few minutes on first run)
echo.

if "%1"=="rebuild" (
    docker-compose down
    docker-compose up -d --build
) else (
    docker-compose up -d
)

echo.
echo Waiting for services to start...
timeout /t 10 /nobreak

echo.
echo ==================================================
echo 🎉 Setup Complete!
echo ==================================================
echo.
echo Services should be running:
echo   - Backend API: http://localhost:8000
echo   - Frontend Dashboard: http://localhost:3000
echo.
echo Try opening http://localhost:3000 in your browser
echo API Documentation: http://localhost:8000/docs
echo.
echo Useful Commands:
echo   - View logs: docker-compose logs -f
echo   - Stop services: docker-compose down
echo   - Rebuild: quickstart.bat rebuild
echo.
