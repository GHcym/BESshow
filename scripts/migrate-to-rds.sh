#!/bin/bash

# BESshow RDS Migration Script

echo "🚀 Starting RDS migration process..."

# Configuration
RDS_ENDPOINT=${RDS_ENDPOINT}
RDS_USERNAME=${RDS_USERNAME}
RDS_PASSWORD=${RDS_PASSWORD}
RDS_DATABASE=${RDS_DATABASE}

# Step 1: Create database dump from current container
echo "📦 Creating database dump..."
docker compose -f docker-compose.staging.yml exec -T bes-rds pg_dump -U besshow -d besshow > besshow_backup.sql

# Step 2: Test RDS connection
echo "🔗 Testing RDS connection..."
PGPASSWORD=$RDS_PASSWORD psql -h $RDS_ENDPOINT -U $RDS_USERNAME -d $RDS_DATABASE -c "SELECT version();"

# Step 3: Import data to RDS
echo "📥 Importing data to RDS..."
PGPASSWORD=$RDS_PASSWORD psql -h $RDS_ENDPOINT -U $RDS_USERNAME -d $RDS_DATABASE < besshow_backup.sql

# Step 4: Update application configuration
echo "⚙️ Updating application configuration..."
export DATABASE_URL="postgresql://$RDS_USERNAME:$RDS_PASSWORD@$RDS_ENDPOINT:5432/$RDS_DATABASE"

# Step 5: Deploy production version
echo "🚀 Deploying production version..."
docker compose -f docker-compose.prod.yml up -d

echo "✅ RDS migration completed!"
echo "🌐 Application available with RDS backend"