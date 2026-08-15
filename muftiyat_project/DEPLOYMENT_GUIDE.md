# DEPLOYMENT_GUIDE.md - Муфтияттын Исламий Портали Deployment

## 🚀 Deployment Guide for Production

### Prerequisites
- Docker & Docker Compose
- Domain name (e.g., muftiyat.kg)
- SSL certificate (Let's Encrypt)
- AWS account (optional, for S3 media storage)
- PostgreSQL 14+ (if not using Docker)
- Redis 7+ (if not using Docker)

---

## 📋 Pre-Deployment Checklist

- [ ] Generate new SECRET_KEY
- [ ] Update .env for production
- [ ] Configure database credentials
- [ ] Set up email configuration
- [ ] Enable HTTPS
- [ ] Configure allowed hosts
- [ ] Set DEBUG=False
- [ ] Run security checks
- [ ] Backup database
- [ ] Configure logging

---

## 🐳 Docker Deployment

### 1. Prepare Production .env

Create `.env` with production values:

```bash
# Copy template
cp .env.example .env

# Edit with production values
nano .env  # or use your editor
```

**Critical production settings:**
```
DEBUG=False
ENVIRONMENT=production
DJANGO_ALLOWED_HOSTS=muftiyat.kg,www.muftiyat.kg
SECRET_KEY=<generate-random-secret-key>
DB_PASSWORD=<strong-random-password>
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
SECURE_HSTS_SECONDS=31536000
```

### 2. Generate Secret Key

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Copy output and add to .env:
```
SECRET_KEY=<generated-key>
```

### 3. Build Production Image

```bash
docker compose build --no-cache
```

### 4. Start Services

```bash
docker compose up -d
```

### 5. Run Migrations

```bash
docker compose exec web python manage.py migrate
```

### 6. Collect Static Files

```bash
docker compose exec web python manage.py collectstatic --noinput --clear
```

### 7. Create Superuser

```bash
docker compose exec web python manage.py createsuperuser
```

### 8. Verify Health

```bash
curl http://localhost/api/v1/health/check/
```

---

## 🔒 SSL/HTTPS Setup (Let's Encrypt)

### 1. Install Certbot

```bash
sudo apt update
sudo apt install certbot python3-certbot-nginx
```

### 2. Generate Certificate

```bash
sudo certbot certonly --standalone -d muftiyat.kg -d www.muftiyat.kg
```

### 3. Update nginx.conf

Add certificate paths:

```nginx
server {
    listen 443 ssl http2;
    server_name muftiyat.kg www.muftiyat.kg;
    
    ssl_certificate /etc/letsencrypt/live/muftiyat.kg/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/muftiyat.kg/privkey.pem;
    
    # SSL configuration...
}
```

### 4. Auto-renew Certificates

```bash
sudo systemctl enable certbot.timer
sudo systemctl start certbot.timer
```

---

## 🌍 AWS Deployment (EC2)

### 1. Create EC2 Instance

```bash
# t3.medium or larger recommended
# Ubuntu 22.04 LTS
# 50GB+ storage
# Security group: Allow 80, 443, 22
```

### 2. Connect to Instance

```bash
ssh -i your-key.pem ubuntu@your-instance-ip
```

### 3. Install Docker

```bash
sudo apt update
sudo apt install docker.io docker-compose git
sudo usermod -aG docker ubuntu
```

### 4. Clone Repository

```bash
git clone <your-repo>
cd muftiyat_project
```

### 5. Setup Environment

```bash
cp .env.example .env
# Edit with AWS RDS database URL and other settings
nano .env
```

### 6. Deploy with Docker

```bash
docker compose -f docker-compose.yml up -d
```

### 7. Configure Domain

Point domain DNS to EC2 Elastic IP

### 8. Setup SSL

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot certonly --standalone -d muftiyat.kg
```

---

## 🗄️ Database Backup & Recovery

### Backup PostgreSQL

```bash
docker compose exec db pg_dump -U muftiyat_user muftiyat_db > backup.sql
```

### Restore from Backup

```bash
cat backup.sql | docker compose exec -T db psql -U muftiyat_user muftiyat_db
```

### Automated Backups

Create backup script:

```bash
#!/bin/bash
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
docker compose exec -T db pg_dump -U muftiyat_user muftiyat_db > \
  backups/backup_$TIMESTAMP.sql
# Keep only last 30 days
find backups/ -name "backup_*.sql" -mtime +30 -delete
```

Add to crontab:
```bash
0 2 * * * /path/to/backup-script.sh
```

---

## 🔍 Monitoring & Logging

### View Real-time Logs

```bash
# All services
docker compose logs -f

# Specific service
docker compose logs -f web
docker compose logs -f db
docker compose logs -f celery
```

### Performance Monitoring

```bash
# Django debug toolbar (development only)
# Enable in settings.py if DEBUG=True

# Celery monitoring
pip install flower
celery -A muftiyat events
# Access at http://localhost:5555
```

### Application Monitoring

```bash
# Health endpoint
curl https://muftiyat.kg/api/v1/health/check/

# Database connection
docker compose exec web python manage.py dbshell

# Static files
ls -la staticfiles/
```

---

## 🔧 Maintenance Tasks

### Run Migrations in Production

```bash
docker compose exec web python manage.py migrate
```

### Collect Static Files

```bash
docker compose exec web python manage.py collectstatic --noinput
```

### Clear Cache

```bash
docker compose exec -T redis redis-cli FLUSHDB
```

### Create/Reset Superuser

```bash
docker compose exec web python manage.py createsuperuser
# or reset password:
docker compose exec web python manage.py changepassword admin_username
```

### Run Custom Commands

```bash
docker compose exec web python manage.py <command_name>
```

---

## 🚨 Troubleshooting

### Services won't start

```bash
# Check Docker status
docker compose ps

# View error logs
docker compose logs web

# Rebuild images
docker compose build --no-cache --pull
docker compose up -d
```

### Database connection error

```bash
# Check database status
docker compose ps db

# Test database connection
docker compose exec db psql -U muftiyat_user -d muftiyat_db -c "SELECT 1"

# Check network
docker network ls
```

### Static files not serving

```bash
# Collect static files
docker compose exec web python manage.py collectstatic --noinput

# Check permissions
docker compose exec -T nginx ls -la /app/staticfiles

# Restart nginx
docker compose restart nginx
```

### Memory issues

```bash
# Check container resource usage
docker stats

# Increase Docker resources in preferences/settings
# Recommended: 4GB+ RAM, 2+ CPU
```

### Celery tasks not running

```bash
# Check Celery worker logs
docker compose logs -f celery

# Check Redis connection
docker compose exec redis redis-cli ping

# Restart Celery
docker compose restart celery
```

---

## 📊 Performance Optimization

### Database
```python
# Add database indexes
python manage.py sqlsequencereset apps.core | \
  docker compose exec -T db psql -U muftiyat_user muftiyat_db

# Optimize queries (use select_related, prefetch_related)
# Monitor query performance
```

### Caching
```bash
# Check Redis memory usage
docker compose exec redis redis-cli info memory

# Clear old cache entries
docker compose exec redis redis-cli FLUSHDB
```

### Static Files
```bash
# Enable CDN in settings
USE_S3=True
AWS_S3_CUSTOM_DOMAIN=your-cdn.com
```

### API Rate Limiting
```nginx
# Already configured in nginx.conf
limit_req_zone $binary_remote_addr zone=api:10m rate=30r/s;
```

---

## 📈 Scaling Considerations

### Horizontal Scaling
```bash
# Run multiple Django instances with load balancer
docker compose up -d --scale web=3
```

### Database Scaling
```bash
# Use AWS RDS for managed PostgreSQL
# Configure master-slave replication
# Use read replicas for analytics
```

### Caching Strategy
```bash
# Use Redis for session storage
# Cache API responses
# Cache template fragments
```

---

## 🔒 Security Hardening

### Update Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt --upgrade
docker compose build --no-cache
```

### Change Default Passwords
```bash
# In .env, change all default passwords
DB_PASSWORD=<new-strong-password>
EMAIL_HOST_PASSWORD=<app-password>
```

### Enable Firewall
```bash
sudo ufw enable
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
```

### Setup Fail2Ban
```bash
sudo apt install fail2ban
# Protects against brute-force attacks
```

---

## 📚 Additional Resources

- Django Deployment: https://docs.djangoproject.com/en/4.2/howto/deployment/
- Docker Best Practices: https://docs.docker.com/develop/dev-best-practices/
- PostgreSQL Administration: https://www.postgresql.org/docs/
- Nginx Configuration: https://nginx.org/en/docs/
- Let's Encrypt: https://letsencrypt.org/docs/

---

## 🎯 Post-Deployment

1. Monitor error logs
2. Set up backup schedule
3. Configure monitoring/alerting
4. Test all API endpoints
5. Verify admin panel access
6. Check email delivery
7. Test user registration
8. Verify static/media files
9. Set up CI/CD pipeline
10. Document custom configurations

---

## 📞 Support & Issues

- GitHub Issues: <your-repo>/issues
- Documentation: README.md
- API Docs: /api/docs/swagger/

---

**Last Updated**: 2024
**Status**: Production Ready
