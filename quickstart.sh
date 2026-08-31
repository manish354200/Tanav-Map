#!/bin/bash
# Quick Start Script for Mental Health Monitoring System

set -e

echo "🚀 Mental Health Monitoring System - Quick Start"
echo "=================================================="
echo ""

# Check prerequisites
echo "Checking prerequisites..."
command -v docker &> /dev/null || { echo "Docker not found. Please install Docker."; exit 1; }
command -v git &> /dev/null || { echo "Git not found. Please install Git."; exit 1; }

echo "✓ Docker and Git found"
echo ""

# Get the project directory
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
echo "Project Directory: $PROJECT_DIR"
echo ""

# Create environment files if they don't exist
echo "Setting up environment files..."

if [ ! -f "$PROJECT_DIR/backend/.env" ]; then
    cp "$PROJECT_DIR/backend/.env.example" "$PROJECT_DIR/backend/.env"
    echo "✓ Created backend/.env"
fi

if [ ! -f "$PROJECT_DIR/frontend/.env" ]; then
    cp "$PROJECT_DIR/frontend/.env.example" "$PROJECT_DIR/frontend/.env"
    echo "✓ Created frontend/.env"
fi

echo ""

# Build and start Docker services
echo "Starting Docker services..."
echo "(This may take a few minutes on first run)"
echo ""

cd "$PROJECT_DIR"

if [ "$1" == "rebuild" ]; then
    docker-compose down
    docker-compose up -d --build
else
    docker-compose up -d
fi

echo ""
echo "Waiting for services to start..."
sleep 10

# Check service health
echo ""
echo "Checking service health..."
echo ""

# Backend health
if curl -s http://localhost:8000/health > /dev/null 2>&1; then
    echo "✓ Backend API: http://localhost:8000"
    echo "  - API Docs: http://localhost:8000/docs"
    echo "  - ReDoc: http://localhost:8000/redoc"
else
    echo "⚠ Backend API not ready yet. Check logs with: docker-compose logs backend"
fi

# Frontend status
if curl -s http://localhost:3000 > /dev/null 2>&1; then
    echo "✓ Frontend: http://localhost:3000"
else
    echo "⚠ Frontend not ready yet. Check logs with: docker-compose logs frontend"
fi

# PostgreSQL status
if docker-compose exec -T postgres pg_isready -U postgres > /dev/null 2>&1; then
    echo "✓ PostgreSQL Database: localhost:5432"
else
    echo "⚠ PostgreSQL not ready yet"
fi

echo ""
echo "=================================================="
echo "🎉 Setup Complete!"
echo "=================================================="
echo ""
echo "Services Running:"
echo "  - Backend API: http://localhost:8000"
echo "  - Frontend Dashboard: http://localhost:3000"
echo "  - PostgreSQL: localhost:5432"
echo "  - MongoDB: localhost:27017"
echo "  - Redis: localhost:6379"
echo ""
echo "Useful Commands:"
echo "  - View logs: docker-compose logs -f"
echo "  - View backend logs: docker-compose logs -f backend"
echo "  - View frontend logs: docker-compose logs -f frontend"
echo "  - Stop services: docker-compose down"
echo "  - Restart services: docker-compose restart"
echo ""
echo "Next Steps:"
echo "  1. Open http://localhost:3000 in your browser"
echo "  2. Check API docs at http://localhost:8000/docs"
echo "  3. Read documentation in docs/ folder"
echo ""
echo "For support, see docs/DEPLOYMENT.md or docs/ARCHITECTURE.md"
echo ""
