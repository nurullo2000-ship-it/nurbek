# Муфтияттын Исламий Портали - API Examples

## Base URL
```
Development: http://localhost:8000/api/v1
Production: https://muftiyat.kg/api/v1
```

## Authentication

### Register New User
```bash
curl -X POST http://localhost:8000/api/v1/users/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "newuser",
    "email": "user@example.com",
    "password": "securepass123",
    "password2": "securepass123",
    "first_name": "Жаныбек",
    "last_name": "Ахметов"
  }'
```

### Get JWT Token
```bash
curl -X POST http://localhost:8000/api/auth/token/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "newuser",
    "password": "securepass123"
  }'

# Response:
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

### Refresh Token
```bash
curl -X POST http://localhost:8000/api/auth/token/refresh/ \
  -H "Content-Type: application/json" \
  -d '{
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
  }'
```

### Verify Token
```bash
curl -X POST http://localhost:8000/api/auth/token/verify/ \
  -H "Content-Type: application/json" \
  -d '{
    "token": "eyJ0eXAiOiJKV1QiLCJhbGc..."
  }'
```

## Users

### Get Current User Profile
```bash
curl -X GET http://localhost:8000/api/v1/users/me/ \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc..."
```

### List All Users (Paginated)
```bash
curl -X GET "http://localhost:8000/api/v1/users/?page=1&page_size=20" \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc..."
```

### Search Users
```bash
curl -X GET "http://localhost:8000/api/v1/users/?search=жаныбек" \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc..."
```

### Filter Users by Role
```bash
curl -X GET "http://localhost:8000/api/v1/users/?role=scholar" \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc..."
```

### Get User Profile
```bash
curl -X GET http://localhost:8000/api/v1/users/1/ \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc..."
```

### Update User Profile
```bash
curl -X PUT http://localhost:8000/api/v1/users/1/ \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc..." \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "Жаныбек",
    "last_name": "Ахметов",
    "bio": "Кыргызстандын мусулман аалымы",
    "city": "Бишкек",
    "country": "Кыргызстан",
    "website": "https://example.com"
  }'
```

### Change Password
```bash
curl -X POST http://localhost:8000/api/v1/users/change_password/ \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc..." \
  -H "Content-Type: application/json" \
  -d '{
    "old_password": "oldpass123",
    "new_password": "newpass123",
    "new_password2": "newpass123"
  }'
```

## Roles

### List All Roles
```bash
curl -X GET http://localhost:8000/api/v1/roles/
```

### Get Role Details
```bash
curl -X GET http://localhost:8000/api/v1/roles/superadmin/
```

## Categories

### List All Categories
```bash
curl -X GET http://localhost:8000/api/v1/categories/
```

### Filter Categories
```bash
curl -X GET "http://localhost:8000/api/v1/categories/?search=жаңылыктар"
```

### Sort Categories
```bash
curl -X GET "http://localhost:8000/api/v1/categories/?ordering=name"
curl -X GET "http://localhost:8000/api/v1/categories/?ordering=-order"
```

### Get Category Details
```bash
curl -X GET http://localhost:8000/api/v1/categories/1/
```

## Tags

### List All Tags
```bash
curl -X GET http://localhost:8000/api/v1/tags/
```

### Search Tags
```bash
curl -X GET "http://localhost:8000/api/v1/tags/?search=исламий"
```

### Get Tag Details
```bash
curl -X GET http://localhost:8000/api/v1/tags/1/
```

## Contact Messages

### Submit Contact Form
```bash
curl -X POST http://localhost:8000/api/v1/contact/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Жаныбек Ахметов",
    "email": "janybek@example.com",
    "phone": "+996555123456",
    "subject": "Диний суроо",
    "message": "Жеңил суроо: Намаз убакыты кандай белгиленет?"
  }'
```

### List Contact Messages (Admin Only)
```bash
curl -X GET http://localhost:8000/api/v1/contact/ \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc..."
```

### Filter by Status (Admin Only)
```bash
curl -X GET "http://localhost:8000/api/v1/contact/?status=new" \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc..."
```

### Mark Message as Read (Admin Only)
```bash
curl -X POST http://localhost:8000/api/v1/contact/1/mark_as_read/ \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc..."
```

### Reply to Message (Admin Only)
```bash
curl -X POST http://localhost:8000/api/v1/contact/1/reply/ \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc..." \
  -H "Content-Type: application/json" \
  -d '{
    "reply": "Сүйөмдүлүк суроо үчүн! Намаз убактылары үйгө байланыштуу өзгөрүлөт..."
  }'
```

## Banners

### List Active Banners
```bash
curl -X GET http://localhost:8000/api/v1/banners/
```

### Filter Banners by Placement
```bash
curl -X GET "http://localhost:8000/api/v1/banners/?placement=homepage"
```

### Get Banner Details
```bash
curl -X GET http://localhost:8000/api/v1/banners/1/
```

## Site Configuration

### Get Site Configuration
```bash
curl -X GET http://localhost:8000/api/v1/config/
```

### Response Example:
```json
{
  "site_title": "Муфтияттын Исламий Портали",
  "site_description": "Кыргызстандагы исламий маалымат жана ресурстар",
  "phone": "+996312-55-00-00",
  "email": "info@muftiyat.kg",
  "address": "Бишкек, Кыргызстан",
  "facebook_url": "https://facebook.com/muftiyat",
  "twitter_url": "https://twitter.com/muftiyat",
  "instagram_url": "https://instagram.com/muftiyat",
  "youtube_url": "https://youtube.com/muftiyat",
  "telegram_url": "https://t.me/muftiyat",
  "maintenance_mode": false
}
```

## Health Check

### Check API Health
```bash
curl -X GET http://localhost:8000/api/v1/health/check/
```

## Python Examples

### Using Python Requests Library
```python
import requests
import json

BASE_URL = "http://localhost:8000/api/v1"

# Register user
def register_user():
    url = f"{BASE_URL}/users/"
    data = {
        "username": "newuser",
        "email": "user@example.com",
        "password": "securepass123",
        "password2": "securepass123"
    }
    response = requests.post(url, json=data)
    return response.json()

# Get token
def get_token(username, password):
    url = "http://localhost:8000/api/auth/token/"
    data = {
        "username": username,
        "password": password
    }
    response = requests.post(url, json=data)
    return response.json()

# Get current user
def get_current_user(token):
    url = f"{BASE_URL}/users/me/"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)
    return response.json()

# Submit contact form
def submit_contact(name, email, subject, message):
    url = f"{BASE_URL}/contact/"
    data = {
        "name": name,
        "email": email,
        "subject": subject,
        "message": message
    }
    response = requests.post(url, json=data)
    return response.json()

# Get categories
def get_categories(page=1):
    url = f"{BASE_URL}/categories/?page={page}"
    response = requests.get(url)
    return response.json()

# Usage
if __name__ == "__main__":
    # Register
    user = register_user()
    print(f"Registered: {user}")
    
    # Get token
    token = get_token("newuser", "securepass123")
    print(f"Token: {token}")
    
    # Get current user
    current_user = get_current_user(token['access'])
    print(f"Current user: {current_user}")
    
    # Submit contact
    contact = submit_contact("John", "john@example.com", "Help", "Need help")
    print(f"Contact: {contact}")
    
    # Get categories
    categories = get_categories()
    print(f"Categories: {categories}")
```

## Error Handling

### Common Error Responses

#### 400 Bad Request
```json
{
  "detail": "Invalid request data",
  "errors": {
    "username": ["This field may not be blank."],
    "password": ["This password is too common."]
  }
}
```

#### 401 Unauthorized
```json
{
  "detail": "Authentication credentials were not provided."
}
```

#### 403 Forbidden
```json
{
  "detail": "You do not have permission to perform this action."
}
```

#### 404 Not Found
```json
{
  "detail": "Not found."
}
```

#### 429 Too Many Requests (Rate Limited)
```json
{
  "detail": "Request was throttled. Expected available in 60 seconds."
}
```

## Rate Limiting

- **Anonymous users**: 100 requests per hour
- **Authenticated users**: 1000 requests per hour
- **API endpoints**: 30 requests per second

## Pagination

All list endpoints support pagination:

```bash
curl "http://localhost:8000/api/v1/users/?page=1&page_size=20"
```

### Response Format
```json
{
  "count": 100,
  "next": "http://localhost:8000/api/v1/users/?page=2",
  "previous": null,
  "results": [...]
}
```

## Filtering & Searching

### Available Filters
- `role` - Filter by user role
- `gender` - Filter by gender
- `city` - Filter by city
- `status` - Filter contact messages by status
- `placement` - Filter banners by placement

### Ordering
```bash
curl "http://localhost:8000/api/v1/users/?ordering=-date_joined"
curl "http://localhost:8000/api/v1/categories/?ordering=name"
```

## Documentation

- **Swagger UI**: http://localhost:8000/api/docs/swagger/
- **ReDoc**: http://localhost:8000/api/docs/redoc/
- **Schema**: http://localhost:8000/api/schema/
