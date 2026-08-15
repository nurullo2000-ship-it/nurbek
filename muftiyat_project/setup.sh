#!/bin/bash
# Setup script for муфтият project
# This script initializes the project for first time use

set -e

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║    Муфтияттын Исламий Портали - PHASE 1 Setup               ║"
echo "╚════════════════════════════════════════════════════════════════╝"

# Function to check if Docker is installed
check_docker() {
    if ! command -v docker &> /dev/null; then
        echo "❌ Docker not found. Please install Docker first."
        exit 1
    fi
    echo "✅ Docker found"
}

# Function to check if Docker Compose is installed
check_docker_compose() {
    if ! command -v docker-compose &> /dev/null; then
        echo "❌ Docker Compose not found. Please install Docker Compose first."
        exit 1
    fi
    echo "✅ Docker Compose found"
}

# Function to setup environment
setup_env() {
    if [ ! -f .env ]; then
        echo "📝 Creating .env file from .env.example..."
        cp .env.example .env
        echo "✅ .env file created"
        echo "⚠️  Please edit .env file with your configuration"
    else
        echo "✅ .env file already exists"
    fi
}

# Function to build and start services
start_services() {
    echo "🚀 Building and starting services..."
    docker compose up --build -d
    
    # Wait for services to be ready
    echo "⏳ Waiting for services to be ready..."
    sleep 10
    
    echo "✅ Services started"
}

# Function to run migrations
run_migrations() {
    echo "📦 Running database migrations..."
    docker compose exec -T web python manage.py migrate
    echo "✅ Migrations completed"
}

# Function to collect static files
collect_static() {
    echo "📦 Collecting static files..."
    docker compose exec -T web python manage.py collectstatic --noinput
    echo "✅ Static files collected"
}

# Function to create superuser
create_superuser() {
    echo "👤 Creating superuser..."
    echo "Please provide superuser credentials:"
    docker compose exec web python manage.py createsuperuser
    echo "✅ Superuser created"
}

# Function to create sample data
create_sample_data() {
    echo "📊 Creating sample data..."
    docker compose exec -T web python manage.py shell << EOF
from apps.core.models import Category, Tag, Role, SiteConfiguration

# Roles are automatically created via signals
print("✅ Default roles created")

# Create categories
categories = [
    {'name': 'Жаңылыктар', 'slug': 'news', 'order': 1},
    {'name': 'Макалалар', 'slug': 'articles', 'order': 2},
    {'name': 'Диний суроо-жооп', 'slug': 'fatwa', 'order': 3},
    {'name': 'Аалымдар', 'slug': 'scholars', 'order': 4},
]

for cat in categories:
    Category.objects.get_or_create(
        name=cat['name'],
        defaults={'slug': cat['slug'], 'order': cat['order']}
    )
print("✅ Categories created")

# Create tags
tags = [
    {'name': 'исламий', 'slug': 'islamic'},
    {'name': 'өндүрүш', 'slug': 'education'},
    {'name': 'здравие', 'slug': 'health'},
    {'name': 'семья', 'slug': 'family'},
]

for tag in tags:
    Tag.objects.get_or_create(
        name=tag['name'],
        defaults={'slug': tag['slug']}
    )
print("✅ Tags created")

# Site configuration is automatically created via signals
print("✅ Site configuration initialized")
EOF
    echo "✅ Sample data created"
}

# Function to display access information
show_info() {
    echo ""
    echo "╔════════════════════════════════════════════════════════════════╗"
    echo "║             🎉 Setup Complete - Access Information           ║"
    echo "╚════════════════════════════════════════════════════════════════╝"
    echo ""
    echo "🌐 Application URLs:"
    echo "   - Homepage: http://localhost/"
    echo "   - Admin Panel: http://localhost/admin/"
    echo "   - API Documentation: http://localhost/api/docs/swagger/"
    echo "   - API ReDoc: http://localhost/api/docs/redoc/"
    echo ""
    echo "📚 API Endpoints:"
    echo "   - Users: http://localhost/api/v1/users/"
    echo "   - Categories: http://localhost/api/v1/categories/"
    echo "   - Tags: http://localhost/api/v1/tags/"
    echo "   - Contact: http://localhost/api/v1/contact/"
    echo ""
    echo "🐳 Docker Commands:"
    echo "   - View logs: docker compose logs -f web"
    echo "   - Run shell: docker compose exec web python manage.py shell"
    echo "   - Stop services: docker compose down"
    echo ""
    echo "📖 Documentation:"
    echo "   - README.md: Complete project documentation"
    echo "   - API_EXAMPLES.md: API usage examples"
    echo "   - QUICK_START.sh: Quick start guide"
    echo ""
}

# Main execution
main() {
    echo ""
    echo "1️⃣  Checking Docker installation..."
    check_docker
    
    echo ""
    echo "2️⃣  Checking Docker Compose installation..."
    check_docker_compose
    
    echo ""
    echo "3️⃣  Setting up environment..."
    setup_env
    
    echo ""
    echo "4️⃣  Starting services..."
    start_services
    
    echo ""
    echo "5️⃣  Running migrations..."
    run_migrations
    
    echo ""
    echo "6️⃣  Collecting static files..."
    collect_static
    
    echo ""
    echo "7️⃣  Creating sample data..."
    create_sample_data
    
    echo ""
    echo "8️⃣  Creating superuser..."
    create_superuser
    
    echo ""
    show_info
    
    echo "✨ Setup complete! Happy coding! 🚀"
}

# Run main function
main
