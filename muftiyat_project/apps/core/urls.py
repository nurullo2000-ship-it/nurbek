"""
URL configuration for core app
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserViewSet, RoleViewSet, ContactMessageViewSet,
    CategoryViewSet, TagViewSet, BannerViewSet,
    SiteConfigurationViewSet, HealthCheckView
)

# Create router for viewsets
router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'roles', RoleViewSet, basename='role')
router.register(r'contact', ContactMessageViewSet, basename='contact')
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'tags', TagViewSet, basename='tag')
router.register(r'banners', BannerViewSet, basename='banner')
router.register(r'config', SiteConfigurationViewSet, basename='site-config')
router.register(r'health', HealthCheckView, basename='health')

urlpatterns = [
    path('', include(router.urls)),
]
