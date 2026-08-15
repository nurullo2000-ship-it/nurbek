# 📚 QUICK_REFERENCE.md - Command Cheat Sheet

## Getting Started

### Docker (Recommended)
```bash
# First time setup
docker compose up --build
docker compose exec web python manage.py createsuperuser

# Start services
docker compose up -d

# Stop services
docker compose down

# View logs
docker compose logs -f web
docker compose logs -f db
docker compose logs -f redis
docker compose logs -f celery

# Access admin
# http://localhost/admin
```

### Local Development
```bash
# Setup
python3.12 -m venv venv
source venv/bin/activate  # or: venv\Scripts\activate (Windows)
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver

# Access admin
# http://localhost:8000/admin
```

---

## Django Commands

```bash
# Database
python manage.py migrate              # Apply migrations
python manage.py makemigrations       # Create migrations
python manage.py showmigrations       # Show migration status
python manage.py sqlsequencereset     # Reset sequences

# Users
python manage.py createsuperuser      # Create admin user
python manage.py changepassword       # Change user password

# Static files
python manage.py collectstatic        # Collect static files
python manage.py findstatic           # Find static files

# Debugging
python manage.py shell                # Interactive Python shell
python manage.py shell_plus           # Shell with IPython
python manage.py dbshell              # Database shell
python manage.py check                # System checks
python manage.py check --deploy       # Production checks

# Management
python manage.py createsuperuser      # Create superuser
python manage.py dumpdata             # Export data
python manage.py loaddata             # Import data
python manage.py clearsessions        # Clear expired sessions
python manage.py flush                # Clear database
```

---

## Testing

```bash
# Run all tests
pytest
python manage.py test

# Run specific app
pytest apps/core/
python manage.py test apps.core

# Run specific test class
pytest apps/core/tests.py::UserModelTest
python manage.py test apps.core.tests.UserModelTest

# Run specific test method
pytest apps/core/tests.py::UserModelTest::test_user_creation
python manage.py test apps.core.tests.UserModelTest.test_user_creation

# With coverage
pytest --cov=apps/core --cov-report=html

# With verbose output
pytest -v
python manage.py test -v 2

# Stop on first failure
pytest -x
python manage.py test --failfast
```

---

## Docker Commands

```bash
# Build
docker compose build                    # Build images
docker compose build --no-cache         # Build without cache

# Start/Stop
docker compose up                       # Start services
docker compose up -d                    # Start in background
docker compose down                     # Stop services
docker compose restart                  # Restart services
docker compose restart web              # Restart specific service

# Logs
docker compose logs                     # Show all logs
docker compose logs -f                  # Follow logs
docker compose logs -f web              # Follow specific service
docker compose logs --tail=50 web       # Last 50 lines

# Execute
docker compose exec web bash            # Open terminal
docker compose exec web python manage.py shell
docker compose exec web python manage.py migrate
docker compose exec web python manage.py createsuperuser

# Clean up
docker compose down -v                  # Remove containers & volumes
docker system prune -a                  # Remove unused images
docker volume prune                     # Remove unused volumes

# Status
docker compose ps                       # Show running containers
docker compose images                   # Show images
docker compose stats                    # Resource usage
```

---

## API Endpoints

### Authentication
```
POST /api/auth/token/                   - Get JWT token
POST /api/auth/token/refresh/           - Refresh token
POST /api/auth/token/verify/            - Verify token
```

### Users
```
POST   /api/v1/users/                   - Register
GET    /api/v1/users/                   - List users
GET    /api/v1/users/{id}/              - Get user
PUT    /api/v1/users/{id}/              - Update user
DELETE /api/v1/users/{id}/              - Delete user
GET    /api/v1/users/me/                - Get current user
POST   /api/v1/users/change_password/   - Change password
```

### Contact
```
POST   /api/v1/contact/                 - Submit form
GET    /api/v1/contact/                 - List (admin)
GET    /api/v1/contact/{id}/            - Get detail
POST   /api/v1/contact/{id}/mark_as_read/  - Mark read (admin)
POST   /api/v1/contact/{id}/reply/      - Reply (admin)
```

### Categories & Tags
```
GET /api/v1/categories/                 - List categories
GET /api/v1/categories/{id}/            - Get category
GET /api/v1/tags/                       - List tags
GET /api/v1/tags/{id}/                  - Get tag
```

### Other
```
GET /api/v1/roles/                      - List roles
GET /api/v1/banners/                    - List banners
GET /api/v1/config/                     - Site config
GET /api/v1/health/check/               - Health check
```

---

## cURL Examples

```bash
# Get token
curl -X POST http://localhost:8000/api/auth/token/ \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"password"}'

# Use token in requests
curl -H "Authorization: Bearer <token>" \
  http://localhost:8000/api/v1/users/

# List with pagination
curl "http://localhost:8000/api/v1/users/?page=1&page_size=20"

# Search
curl "http://localhost:8000/api/v1/users/?search=john"

# Filter
curl "http://localhost:8000/api/v1/users/?role=admin"

# Order
curl "http://localhost:8000/api/v1/users/?ordering=-date_joined"
```

---

## Code Formatting & Linting

```bash
# Format code
black .

# Sort imports
isort .

# Lint
flake8 .

# Type checking
mypy apps/

# All together
black . && isort . && flake8 . && mypy apps/
```

---

## File Locations

```
Project Root
├── manage.py                    # Run commands here
├── requirements.txt             # Python packages
├── .env                         # Environment variables
├── docker-compose.yml           # Docker config
│
├── muftiyat/                    # Project settings
│   ├── settings.py              # Main config
│   ├── urls.py                  # URL routing
│   └── wsgi.py                  # WSGI app
│
├── apps/                        # Django apps
│   └── core/                    # Core app
│       ├── models.py            # Database models
│       ├── views.py             # API views
│       ├── urls.py              # App URLs
│       ├── admin.py             # Admin panel
│       ├── tests.py             # Tests
│       └── migrations/          # Database migrations
│
├── templates/                   # HTML templates
├── staticfiles/                 # Static files
├── media/                       # Uploads
├── logs/                        # Log files
└── locale/                      # Translations
```

---

## Important URLs

```
Development:
- Homepage: http://localhost:8000/
- Admin: http://localhost:8000/admin/
- API: http://localhost:8000/api/v1/
- Docs: http://localhost:8000/api/docs/swagger/

Docker:
- Homepage: http://localhost/
- Admin: http://localhost/admin/
- API: http://localhost/api/v1/
- Docs: http://localhost/api/docs/swagger/
```

---

## Environment Variables

```bash
# Core
DEBUG=True                              # Debug mode
SECRET_KEY=<your-secret-key>           # Django secret
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DB_ENGINE=django.db.backends.postgresql
DB_NAME=muftiyat_db
DB_USER=muftiyat_user
DB_PASSWORD=<password>
DB_HOST=localhost
DB_PORT=5432

# Redis
REDIS_URL=redis://localhost:6379/0

# Email
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_HOST_USER=<email>
EMAIL_HOST_PASSWORD=<password>

# Security (Production)
SECURE_SSL_REDIRECT=False
SESSION_COOKIE_SECURE=False
CSRF_COOKIE_SECURE=False
```

---

## Common Issues

### Port Already in Use
```bash
# Find process
lsof -i :8000
# Kill process
kill -9 <PID>
# Or use different port
python manage.py runserver 8001
```

### Database Connection Error
```bash
# Check PostgreSQL
psql -U muftiyat_user -d muftiyat_db
# Or reset (Docker)
docker compose down -v
docker compose up
```

### Static Files Not Loading
```bash
# Collect static files
python manage.py collectstatic --noinput
# Check location
ls -la staticfiles/
```

### Permission Denied
```bash
# Fix file permissions
chmod +x manage.py
chmod +x setup.sh
chmod +x QUICK_START.sh
```

### Module Not Found
```bash
# Install dependencies
pip install -r requirements.txt
# Or in Docker
docker compose build --no-cache
```

---

## Performance Tips

```bash
# Enable query logging
python manage.py shell
from django.db import connection
from django.test.utils import override_settings

# Use select_related for ForeignKey
Article.objects.select_related('category').all()

# Use prefetch_related for ManyToMany
Article.objects.prefetch_related('tags').all()

# Use only() to limit fields
User.objects.only('username', 'email')

# Use values() for dictionaries
User.objects.values('username', 'email')

# Use exists() to check existence
if User.objects.filter(username='admin').exists():
    pass
```

---

## Useful Commands Summary

| Task | Command |
|------|---------|
| Run server | `python manage.py runserver` |
| Run tests | `pytest` |
| Create admin | `python manage.py createsuperuser` |
| Migrate | `python manage.py migrate` |
| Make migrations | `python manage.py makemigrations` |
| Start Docker | `docker compose up -d` |
| View logs | `docker compose logs -f web` |
| Open shell | `python manage.py shell_plus` |
| Format code | `black .` |
| Lint | `flake8 .` |
| Type check | `mypy apps/` |

---

## Documentation Files

| File | Purpose |
|------|---------|
| README.md | Complete guide |
| API_EXAMPLES.md | API examples |
| DEPLOYMENT_GUIDE.md | Production deployment |
| PROJECT_STRUCTURE.md | Directory structure |
| QUICK_START.sh | Commands reference |
| setup.sh | Auto setup |

---

## Need Help?

1. **Read Documentation**: Check README.md or specific guide
2. **Check Logs**: `docker compose logs -f web`
3. **Test Endpoint**: Use Swagger UI at `/api/docs/swagger/`
4. **Run Tests**: `pytest -v` to debug issues
5. **Django Shell**: `python manage.py shell_plus` to inspect data

---

**Last Updated**: 2024
**Version**: 1.0.0-PHASE1
