#!/bin/bash
# Quick start guide for Муфтияттын Исламий Портали
# This script contains all the commands needed to get the project running

# ============================================================================
# 1. LOCAL DEVELOPMENT SETUP
# ============================================================================

echo "=== PHASE 1: Local Development Setup ==="

# 1.1 Create virtual environment
echo "Creating virtual environment..."
python3.12 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 1.2 Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# 1.3 Create .env file
echo "Setting up environment variables..."
cp .env.example .env
# Edit .env manually

# 1.4 Create migrations
echo "Creating database migrations..."
python manage.py migrate

# 1.5 Create superuser
echo "Creating superuser..."
python manage.py createsuperuser

# 1.6 Create default roles and configuration
echo "Creating default roles and site configuration..."
python manage.py shell << EOF
from apps.core.models import Role, SiteConfiguration

# Roles are created automatically via signals
print("✅ Roles created")

# Site configuration
config = SiteConfiguration.get_instance()
print("✅ Site configuration initialized")
EOF

# 1.7 Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# 1.8 Run development server
echo "Starting development server..."
python manage.py runserver

# ============================================================================
# 2. DOCKER SETUP (RECOMMENDED)
# ============================================================================

echo "=== PHASE 2: Docker Setup ==="

# 2.1 Build and start containers
echo "Building and starting containers..."
docker compose up --build

# 2.2 In another terminal, create superuser
echo "Creating superuser in Docker..."
docker compose exec web python manage.py createsuperuser

# 2.3 Check logs
echo "Checking logs..."
docker compose logs -f web

# ============================================================================
# 3. DATABASE MANAGEMENT
# ============================================================================

echo "=== PHASE 3: Database Management ==="

# 3.1 Make migrations
echo "Making migrations..."
python manage.py makemigrations

# 3.2 Apply migrations
echo "Applying migrations..."
python manage.py migrate

# 3.3 Show migration status
echo "Migration status..."
python manage.py showmigrations

# 3.4 Reverse migrations (if needed)
echo "Reversing migrations (example)..."
python manage.py migrate apps.core 0001

# ============================================================================
# 4. ADMIN PANEL MANAGEMENT
# ============================================================================

echo "=== PHASE 4: Admin Panel Management ==="

# 4.1 Create initial data in admin
echo "Creating initial categories..."
python manage.py shell << EOF
from apps.core.models import Category, Tag

# Create categories
categories = [
    {'name': 'Жаңылыктар', 'slug': 'news'},
    {'name': 'Макалалар', 'slug': 'articles'},
    {'name': 'Диний суроо-жооп', 'slug': 'fatwa'},
]

for cat in categories:
    Category.objects.get_or_create(
        name=cat['name'],
        defaults={'slug': cat['slug']}
    )

# Create tags
tags = [
    {'name': 'исламий', 'slug': 'islamic'},
    {'name': 'образование', 'slug': 'education'},
    {'name': 'здравие', 'slug': 'health'},
]

for tag in tags:
    Tag.objects.get_or_create(
        name=tag['name'],
        defaults={'slug': tag['slug']}
    )

print("✅ Initial data created")
EOF

# 4.2 Access admin panel
echo "🌐 Admin panel is available at:"
echo "http://localhost:8000/admin/"

# ============================================================================
# 5. API TESTING
# ============================================================================

echo "=== PHASE 5: API Testing ==="

# 5.1 API documentation
echo "📚 API Documentation available at:"
echo "http://localhost:8000/api/docs/swagger/"
echo "http://localhost:8000/api/docs/redoc/"

# 5.2 Test endpoints
echo "Testing API endpoints..."

# Register new user
curl -X POST http://localhost:8000/api/v1/users/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "testpass123",
    "password2": "testpass123"
  }'

# Get categories
curl http://localhost:8000/api/v1/categories/

# Get site configuration
curl http://localhost:8000/api/v1/config/

# ============================================================================
# 6. TESTING
# ============================================================================

echo "=== PHASE 6: Testing ==="

# 6.1 Run all tests
echo "Running all tests..."
pytest

# 6.2 Run specific app tests
echo "Running core app tests..."
pytest apps/core/tests.py -v

# 6.3 Run with coverage
echo "Running tests with coverage..."
pytest --cov=apps/core --cov-report=html

# 6.4 Django test runner
echo "Running Django tests..."
python manage.py test apps.core

# ============================================================================
# 7. CELERY SETUP
# ============================================================================

echo "=== PHASE 7: Celery Setup ==="

# 7.1 Run Celery worker (separate terminal)
echo "Starting Celery worker..."
celery -A muftiyat worker -l info

# 7.2 Run Celery beat (separate terminal)
echo "Starting Celery beat..."
celery -A muftiyat beat -l info

# 7.3 Monitor Celery
echo "Monitoring Celery (flower)..."
pip install flower
celery -A muftiyat events --loglevel=info

# ============================================================================
# 8. SECURITY & PRODUCTION
# ============================================================================

echo "=== PHASE 8: Security & Production ==="

# 8.1 Generate secret key
echo "Generating Django secret key..."
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

# 8.2 Run security checks
echo "Running security checks..."
python manage.py check --deploy

# 8.3 Collect static files (production)
echo "Collecting static files for production..."
python manage.py collectstatic --noinput --clear

# 8.4 Run Django shell for debugging
echo "Opening Django shell..."
python manage.py shell_plus

# ============================================================================
# 9. DOCKER COMMANDS
# ============================================================================

echo "=== PHASE 9: Docker Commands ==="

# 9.1 Build images
echo "Building Docker images..."
docker compose build

# 9.2 Start services
echo "Starting services..."
docker compose up -d

# 9.3 Stop services
echo "Stopping services..."
docker compose down

# 9.4 Restart services
echo "Restarting services..."
docker compose restart

# 9.5 Run commands in container
echo "Running command in web container..."
docker compose exec web python manage.py migrate

# 9.6 View logs
echo "Viewing logs..."
docker compose logs -f web
docker compose logs -f db
docker compose logs -f redis
docker compose logs -f celery

# ============================================================================
# 10. USEFUL COMMANDS
# ============================================================================

echo "=== PHASE 10: Useful Commands ==="

# Format code with black
black .

# Sort imports
isort .

# Check code quality
flake8 .

# Type checking
mypy .

# Create database backup
pg_dump muftiyat_db > backup.sql

# Restore database
psql muftiyat_db < backup.sql

echo "✅ All commands documented!"
