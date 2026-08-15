# Муфтияттын Исламий Портали 🕌

Заманбап, production-ready исламий маалымат порталы Кыргызстан үчүн.

## Жалпы маалымат

Бул проект Кыргызстандагы Муфтияттын деңгээлинде заманбап исламий маалымат портали. Сайт төмөнкүлөрдү қамтыйды:

- 📰 Диний жаңылыктар
- 📄 Макалалар жана ресурстар
- 🤔 Диний суроо-жооп система
- 👨‍🎓 Аалымдар тууралуу маалымат
- 🕌 Мечиттердин каталогу жана картасы
- 🕐 Намаз убактыларын эсептөө
- 📖 Куран тексттери жана котормолору
- 📚 Хадис жыйнактары
- 💰 Зекет калькулятору
- 🛫 Ажылык жана умра гайд
- 📽️ Видео жана аудио контент
- 🎨 Сүрөт галерея
- 📢 Жарыялар жана иш-чаралар
- 🌐 3 тилди колдоо (кыргызча, орусча, арабча)

## 🛠️ Технологиялар

### Backend
- **Python 3.12+** - Programming language
- **Django 4.2** - Web framework
- **Django REST Framework** - API framework
- **PostgreSQL** - Database
- **Redis** - Caching and message broker
- **Celery** - Task queue
- **Gunicorn** - WSGI server

### Frontend (Ready for Phase 11)
- **HTML5** - Markup
- **CSS3** - Styling
- **JavaScript** - Client-side logic
- **Bootstrap 5** - Responsive framework
- *(Optional: React for advanced features)*

### DevOps & Deployment
- **Docker** - Containerization
- **Docker Compose** - Orchestration
- **Nginx** - Reverse proxy & web server
- **AWS S3** - Media storage (optional)

### Development Tools
- **pytest** - Testing framework
- **Black** - Code formatter
- **flake8** - Linter
- **isort** - Import sorter
- **mypy** - Type checker

## 📋 Талаптар

### Система талаптары
- Docker & Docker Compose
- Python 3.12+ (local development)
- PostgreSQL 14+ (local development)
- Redis 7+ (local development)

## 🚀 Орнотуу

### 1. Repository клонунуу
```bash
git clone <repository-url>
cd muftiyat_project
```

### 2. Окружение аралык өзгөрүүлөрүн орнотуу
```bash
cp .env.example .env
# Edit .env with your values
```

### 3. Docker менен иштетүү (RECOMMENDED)

#### Биринчи иштетүү
```bash
docker compose up --build
```

Sistem автоматикалык түрдө:
- Бөлмө түзөт
- Миграцияларды өткөрөт
- Статикалык файлдарды жыйнайт
- Django Admin'ди түзөт
- Redis жана Celery'ди баштайт

#### Админ каттоо түзүү
```bash
docker compose exec web python manage.py createsuperuser
```

#### Миграцияларды колдонуу
```bash
# Миграциялар автоматикалык түрдө иштейт, бирок кол менен:
docker compose exec web python manage.py migrate

# Миграция файллары түзүү
docker compose exec web python manage.py makemigrations

# Миграциялар статусун көрүү
docker compose exec web python manage.py showmigrations
```

#### Статикалык файлдарды жыйнау
```bash
docker compose exec web python manage.py collectstatic --noinput
```

#### Django shell'ге кирүү
```bash
docker compose exec web python manage.py shell
# же ipython менен (орнотулган)
docker compose exec web python manage.py shell_plus
```

#### Логдорду көрүү
```bash
docker compose logs -f web     # Django logs
docker compose logs -f celery  # Celery logs
docker compose logs -f nginx   # Nginx logs
```

### 4. Локалдык өндүрүштүк окружениеде иштетүү (Development)

#### Virtual environment түзүү
```bash
python3.12 -m venv venv
source venv/bin/activate  # Linux/Mac
# же
venv\Scripts\activate  # Windows
```

#### Зависимостиларды орнотуу
```bash
pip install -r requirements.txt
```

#### Окружение аралык өзгөрүүлөрүн орнотуу
```bash
cp .env.example .env
# Локальдык PostgreSQL жана Redis үчүн .env өзгөртүү:
# DB_HOST=localhost
# REDIS_URL=redis://localhost:6379/0
```

#### Миграцияларды жүргүзүү
```bash
python manage.py migrate
```

#### Админ каттоо түзүү
```bash
python manage.py createsuperuser
```

#### Django development сервери баштоо
```bash
python manage.py runserver
```

Сайт доступ болот: **http://127.0.0.1:8000/**

#### Celery worker баштоо (башка терминалда)
```bash
celery -A muftiyat worker -l info
```

#### Celery beat баштоо (расписанные задачи үчүн)
```bash
celery -A muftiyat beat -l info
```

## 🌐 API Endpoints

### PHASE 1 - Core API

#### Users
- `POST /api/v1/users/` - Register new user
- `GET /api/v1/users/` - List users (authenticated)
- `GET /api/v1/users/{id}/` - Get user detail
- `PUT /api/v1/users/{id}/` - Update user profile
- `DELETE /api/v1/users/{id}/` - Delete user account
- `GET /api/v1/users/me/` - Get current user profile
- `POST /api/v1/users/change_password/` - Change password

#### Authentication
- `POST /api/auth/token/` - Get JWT token
- `POST /api/auth/token/refresh/` - Refresh token
- `POST /api/auth/token/verify/` - Verify token

#### Contact Messages
- `POST /api/v1/contact/` - Submit contact form
- `GET /api/v1/contact/` - List messages (admin only)
- `GET /api/v1/contact/{id}/` - Get message detail
- `POST /api/v1/contact/{id}/mark_as_read/` - Mark as read (admin)
- `POST /api/v1/contact/{id}/reply/` - Reply to message (admin)

#### Categories
- `GET /api/v1/categories/` - List categories
- `GET /api/v1/categories/{id}/` - Get category detail

#### Tags
- `GET /api/v1/tags/` - List tags
- `GET /api/v1/tags/{id}/` - Get tag detail

#### Banners
- `GET /api/v1/banners/` - List banners
- `GET /api/v1/banners/{id}/` - Get banner detail

#### Site Configuration
- `GET /api/v1/config/` - Get site configuration

#### Health Check
- `GET /api/v1/health/check/` - API health status

### API Documentation
- **Swagger UI**: http://localhost:8000/api/docs/swagger/
- **ReDoc**: http://localhost:8000/api/docs/redoc/
- **Schema**: http://localhost:8000/api/schema/

## 👤 Пайдалануучу Рольдор

### Ролдун системасы
1. **SUPERADMIN** - Толук системалык доступу
2. **ADMIN** - Административдик функциялар
3. **EDITOR** - Контент түзүү жана редактирлөө
4. **MODERATOR** - Контентти модерирлөө
5. **SCHOLAR** - Диний суроолорго жооп берүү
6. **USER** - Стандарттык пайдалануучу (окуу жана байланыш)

## 📝 Environment Variables

Толук `.env` файлдын параметрлери:

```
# Django
DEBUG=True
SECRET_KEY=your-secret-key
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1
ENVIRONMENT=development

# Database
DB_ENGINE=django.db.backends.postgresql
DB_NAME=muftiyat_db
DB_USER=muftiyat_user
DB_PASSWORD=password
DB_HOST=localhost
DB_PORT=5432

# Redis
REDIS_URL=redis://localhost:6379/0
REDIS_HOST=localhost
REDIS_PORT=6379

# Celery
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0

# Email
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-password

# JWT
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_LIFETIME_MINUTES=60
JWT_REFRESH_TOKEN_LIFETIME_DAYS=7

# AWS S3 (production)
USE_S3=False
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
AWS_STORAGE_BUCKET_NAME=

# API
API_PAGINATION_PAGE_SIZE=20
API_MAX_PAGE_SIZE=100

# Localization
LANGUAGE_CODE=ky
TIME_ZONE=Asia/Bishkek

# Security (production)
SECURE_SSL_REDIRECT=False
SECURE_HSTS_SECONDS=0
```

## 🧪 Тестирование

### Pytest менен тестирование чалуу
```bash
# Бардык тесттер
pytest

# Конкреттүу app үчүн
pytest apps/core/tests.py

# Coverage отчету менен
pytest --cov=apps/core

# Аг маска өзгөрүү
pytest -v
```

### Django Test Framework менен
```bash
python manage.py test apps.core
python manage.py test apps.core.tests.UserModelTest
python manage.py test apps.core.tests.UserAPITest.test_user_registration
```

## 📚 Admin Panel

### Доступ
- URL: **http://localhost:8000/admin/**
- Пайдалануучу: Ар бир элеги өзүңүз түзгөн superuser

### Админ функциялары (PHASE 1)
- 👥 Пайдалануучулар башкаруу
- 🔐 Рольдор жана мээстери
- 💬 Байланыш билдирүүлөрүн башкаруу
- 🏷️ Категориялар жана тегдер
- 📢 Баннерлер
- ⚙️ Сайт конфигурациясы
- 📊 SEO Metadata

## 🔒 Коопсуздук

### Реализацияланган коопсуздук өлчөмдөрү
- ✅ CSRF protection
- ✅ XSS protection
- ✅ SQL injection prevention (ORM)
- ✅ Secure password hashing (PBKDF2)
- ✅ JWT token rotation
- ✅ Rate limiting (Nginx)
- ✅ Permission checks (role-based)
- ✅ Secure file uploads
- ✅ HTTPS-ready configuration
- ✅ Environment variables for secrets

### Production Коопсуздук Өндүрүш чеки-листи
```bash
# SECRET_KEY чалуу
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

# .env файлда SECRET_KEY орнотуу
SECRET_KEY=your-generated-secret-key

# Production режимин включить
DEBUG=False
ENVIRONMENT=production

# HTTPS арналарын включить
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
SECURE_HSTS_SECONDS=31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS=True
SECURE_HSTS_PRELOAD=True
```

## 📊 Database Schema (PHASE 1)

### Core Models
- **User** - Пайдалануучулар (AbstractUser basis)
- **Role** - Рольдор жана мээстер
- **ContactMessage** - Байланыш формасы
- **Category** - Контент категориялары
- **Tag** - Контент теглери
- **Banner** - Вебсайт баннерлери
- **SiteConfiguration** - Глобалдык конфигурация
- **SEOMetadata** - SEO маалыматтары

### Database Migrations
```bash
# Миграциялар абалын көрүү
docker compose exec web python manage.py showmigrations

# Бел миграцияны колдонуу
docker compose exec web python manage.py migrate apps.core 0001

# Миграцияны болуп жиберүү
docker compose exec web python manage.py migrate apps.core 0001_initial
```

## 📁 Проект Структурасы

```
muftiyat_project/
├── manage.py                 # Django management script
├── requirements.txt          # Python dependencies
├── .env.example             # Example environment variables
├── .gitignore               # Git ignore rules
├── docker-compose.yml       # Docker Compose configuration
├── Dockerfile               # Docker image definition
├── nginx.conf               # Nginx configuration
├── README.md                # This file
│
├── muftiyat/                # Project settings package
│   ├── __init__.py
│   ├── settings.py          # Django settings
│   ├── urls.py              # Main URL router
│   ├── wsgi.py              # WSGI configuration
│   ├── asgi.py              # ASGI configuration
│   ├── celery.py            # Celery configuration
│   └── schema_hooks.py      # DRF Spectacular hooks
│
├── apps/                    # Django applications
│   ├── __init__.py
│   │
│   ├── core/                # Core application (PHASE 1)
│   │   ├── __init__.py
│   │   ├── apps.py          # App configuration
│   │   ├── models.py        # Core models
│   │   ├── serializers.py   # DRF serializers
│   │   ├── views.py         # API views
│   │   ├── urls.py          # App URLs
│   │   ├── admin.py         # Admin customization
│   │   ├── signals.py       # Django signals
│   │   ├── tests.py         # Unit tests
│   │   ├── migrations/      # Database migrations
│   │   └── management/      # Management commands
│   │
│   ├── users/               # (PHASE 2)
│   ├── news/                # (PHASE 3)
│   ├── articles/            # (PHASE 3)
│   ├── scholars/            # (PHASE 4)
│   ├── fatwa/               # (PHASE 4)
│   ├── mosques/             # (PHASE 5)
│   ├── prayer/              # (PHASE 6)
│   ├── quran/               # (PHASE 7)
│   ├── hadith/              # (PHASE 7)
│   ├── zakat/               # (PHASE 8)
│   ├── hajj/                # (PHASE 8)
│   ├── media/               # (PHASE 9)
│   ├── events/              # (PHASE 9)
│   ├── announcements/       # (PHASE 9)
│   ├── search/              # (PHASE 10)
│   └── pages/               # (PHASE 11)
│
├── templates/               # HTML templates
│   ├── base.html
│   ├── home.html
│   └── ...
│
├── staticfiles/             # Collected static files (auto-generated)
├── media/                   # User uploaded files
├── logs/                    # Application logs
└── locale/                  # Translation files
```

## 🔄 Жумушуу Фазалары

### ✅ PHASE 1: Архитектура + Django Setup + PostgreSQL + Docker
- ✅ Project structure
- ✅ Django configuration
- ✅ PostgreSQL integration
- ✅ Redis caching
- ✅ Docker setup
- ✅ Core models (User, Role, ContactMessage, etc.)
- ✅ Admin panel
- ✅ Core API endpoints
- ✅ Basic authentication

### 📋 PHASE 2: Users + Roles + Authentication
- [ ] Advanced authentication (OAuth, Social login)
- [ ] User profile customization
- [ ] Two-factor authentication
- [ ] User notifications system

### 📋 PHASE 3: News + Articles + Categories
- [ ] News management
- [ ] Article publishing system
- [ ] Category management
- [ ] Comment system

### 📋 PHASE 4: Scholars + Fatwa System
- [ ] Scholar profiles
- [ ] Fatwa question submission
- [ ] Answer management
- [ ] Publication workflow

### 📋 PHASE 5: Mosques + Map Integration
- [ ] Mosque directory
- [ ] Google Maps integration
- [ ] Geolocation features
- [ ] Near me search

### 📋 PHASE 6: Prayer Times
- [ ] Prayer time calculation
- [ ] Location selection
- [ ] Notification system
- [ ] Prayer time API

### 📋 PHASE 7: Quran + Hadith
- [ ] Quran chapters and verses
- [ ] Multiple translations
- [ ] Audio support
- [ ] Hadith collections

### 📋 PHASE 8: Zakat Calculator + Hajj/Umrah
- [ ] Zakat calculation engine
- [ ] Asset input interface
- [ ] Hajj guide system
- [ ] Umrah information

### 📋 PHASE 9: Media + Events + Announcements
- [ ] Video management
- [ ] Audio management
- [ ] Gallery system
- [ ] Event calendar
- [ ] Announcement system

### 📋 PHASE 10: Search + SEO
- [ ] Global search engine
- [ ] Advanced filtering
- [ ] SEO optimization
- [ ] Sitemap generation

### 📋 PHASE 11: Frontend Design
- [ ] Homepage design
- [ ] Responsive layout
- [ ] User interface
- [ ] Frontend optimization

### 📋 PHASE 12: Security + Performance
- [ ] Security audit
- [ ] Performance optimization
- [ ] Load testing
- [ ] Caching strategy

### 📋 PHASE 13: Testing
- [ ] Unit tests
- [ ] Integration tests
- [ ] API tests
- [ ] End-to-end tests

### 📋 PHASE 14: Production Deployment
- [ ] AWS setup
- [ ] CI/CD pipeline
- [ ] Monitoring
- [ ] Backup strategy

## 🚢 Production Deployment

### Docker менен Deploy
```bash
# Production docker compose файлын түзүү
cp docker-compose.yml docker-compose.prod.yml

# Production режимде иштетүү
docker compose -f docker-compose.prod.yml up -d

# Логдорду көрүү
docker compose -f docker-compose.prod.yml logs -f web
```

### AWS EC2 Deploy
```bash
# Instance түзүү
# SSH туюнтуу
ssh -i key.pem ubuntu@your-instance

# Зависимостиларды орнотуу
sudo apt update && sudo apt install docker.io docker-compose git

# Repository клонунуу
git clone <your-repo>
cd muftiyat_project

# Production .env орнотуу
cp .env.example .env
# Edit .env for production

# Docker менен баштоо
sudo docker compose up -d

# SSL сертификат орнотуу (Let's Encrypt)
sudo certbot certonly --standalone -d yourdomain.kg
```

### Nginx конфигурация (Production)
```nginx
server {
    listen 443 ssl http2;
    server_name muftiyat.kg;
    
    ssl_certificate /etc/letsencrypt/live/muftiyat.kg/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/muftiyat.kg/privkey.pem;
    
    location / {
        proxy_pass http://web:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}

# HTTP -> HTTPS redirect
server {
    listen 80;
    server_name muftiyat.kg;
    return 301 https://$server_name$request_uri;
}
```

## 📞 Колдоо жана Контакты

- 📧 Email: support@muftiyat.kg
- 🌐 Website: www.muftiyat.kg
- 📱 Telegram: @muftiyat_support

## 📄 License

Бул проект Apache License 2.0 менен лицензия ээси.

## 👨‍💼 Contributors

- Senior Full-Stack Developer
- UI/UX Designer
- System Architect
- DevOps Engineer

---

**Акыркы жаңылоо**: 2024 жыл
**Версия**: 1.0.0-PHASE1
**Статус**: Production Ready (PHASE 1 Complete)
