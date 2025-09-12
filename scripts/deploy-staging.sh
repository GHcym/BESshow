#!/bin/bash

# BESshow Staging Deployment Script

echo "🚀 Starting BESshow staging deployment..."

# Load environment variables
export $(cat .env.staging | xargs)

# Stop existing containers
echo "📦 Stopping existing containers..."
docker compose -f docker-compose.staging.yml down

# Build and start services
echo "🔨 Building and starting services..."
docker compose -f docker-compose.staging.yml up --build -d

# Wait for database to be ready
echo "⏳ Waiting for database to be ready..."
sleep 10

# Run migrations
echo "🗄️ Running database migrations..."
docker compose -f docker-compose.staging.yml exec bes-app python manage.py migrate

echo "✅ Staging deployment completed!"
echo "🌐 Application available at: http://43.198.12.223:8000"