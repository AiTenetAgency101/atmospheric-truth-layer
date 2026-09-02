#!/bin/bash
# JARVIS Atmospheric Truth Layer - Git Sync & Docker Deploy

echo "🤖 JARVIS - DOCKER DEPLOYMENT SEQUENCE"
echo ""

# Git operations
echo "📡 Git: Pulling latest..."
git pull origin master

echo "📡 Git: Staging changes..."
git add -A

echo "📡 Git: Committing..."
git commit -m "feat: JARVIS Docker deployment $(date '+%Y-%m-%d %H:%M:%S')" || true

echo "📡 Git: Pushing to GitHub..."
git push origin master

# Docker operations
echo ""
echo "🐳 Docker: Building image..."
docker-compose build

echo "🐳 Docker: Starting container..."
docker-compose up -d

echo "🐳 Docker: Checking health..."
sleep 5
docker-compose ps

echo ""
echo "✅ JARVIS SEALED IN DOCKER"
echo "📡 Browser: http://localhost:3001/"
echo "🎬 YouTube: Ready to stream"
echo ""
