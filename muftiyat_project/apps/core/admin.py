"""
Admin panel configuration for core app
"""

from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.utils.html import format_html
from .models import (
    User, Role, ContactMessage, Category, Tag,
    SiteConfiguration, Banner, SEOMetadata
)


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'get_permissions_count')
    search_fields = ('name', 'description')
    filter_horizontal = ('permissions',)
    
    def get_permissions_count(self, obj):
        return obj.permissions.count()
    get_permissions_count.short_description = _('Мээстер саны')


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'get_full_name', 'role', 'is_active', 'email_verified')
    list_filter = ('role', 'is_active', 'email_verified', 'phone_verified', 'gender', 'date_joined')
    search_fields = ('username', 'email', 'first_name', 'last_name', 'phone_number')
    readonly_fields = ('date_joined', 'last_login', 'created_at', 'updated_at')
    
    fieldsets = (
        (_('Негизги маалымат'), {
            'fields': ('username', 'email', 'password', 'first_name', 'last_name')
        }),
        (_('Профиль'), {
            'fields': ('avatar', 'bio', 'gender', 'birth_date', 'city', 'country', 'website', 'is_public'),
            'classes': ('collapse',)
        }),
        (_('Ролдору жана мээстери'), {
            'fields': ('role', 'is_staff', 'is_superuser', 'groups')
        }),
        (_('Статусу'), {
            'fields': ('is_active', 'email_verified', 'phone_verified', 'phone_number', 'newsletter')
        }),
        (_('Социалдык сеттер'), {
            'fields': ('social_id',),
            'classes': ('collapse',)
        }),
        (_('Метадаттар'), {
            'fields': ('date_joined', 'last_login', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    ordering = ('-date_joined',)


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('subject', 'name', 'email', 'status', 'get_colored_status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('name', 'email', 'subject', 'message')
    readonly_fields = ('created_at', 'updated_at', 'email', 'name', 'phone', 'subject', 'message')
    
    fieldsets = (
        (_('Отправитель маалымат'), {
            'fields': ('name', 'email', 'phone')
        }),
        (_('Билдирүү'), {
            'fields': ('subject', 'message')
        }),
        (_('Жооп'), {
            'fields': ('status', 'reply')
        }),
        (_('Метадаттар'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_colored_status(self, obj):
        colors = {
            'new': '#0066cc',
            'read': '#666666',
            'replied': '#009900',
            'closed': '#999999',
        }
        color = colors.get(obj.status, '#000000')
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            color,
            obj.get_status_display()
        )
    get_colored_status.short_description = _('Статусу')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'get_color_preview', 'order', 'is_active')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    
    fieldsets = (
        (_('Негизги маалымат'), {
            'fields': ('name', 'slug', 'description')
        }),
        (_('Дизайн'), {
            'fields': ('icon', 'color', 'order'),
            'classes': ('collapse',)
        }),
        (_('Статусу'), {
            'fields': ('is_active',)
        }),
    )
    
    def get_color_preview(self, obj):
        return format_html(
            '<div style="width: 20px; height: 20px; background-color: {}; border-radius: 3px; display: inline-block;"></div>',
            obj.color
        )
    get_color_preview.short_description = _('Түсү')


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(SiteConfiguration)
class SiteConfigurationAdmin(admin.ModelAdmin):
    list_display = ('site_title', 'maintenance_mode')
    
    fieldsets = (
        (_('Сайттын маалымат'), {
            'fields': ('site_title', 'site_description', 'site_logo', 'site_icon')
        }),
        (_('Байланыш маалымат'), {
            'fields': ('phone', 'email', 'address')
        }),
        (_('Социалдык сеттер'), {
            'fields': ('facebook_url', 'twitter_url', 'instagram_url', 'youtube_url', 'telegram_url'),
            'classes': ('collapse',)
        }),
        (_('API жана интеграциялар'), {
            'fields': ('google_analytics_id', 'google_maps_api_key'),
            'classes': ('collapse',)
        }),
        (_('Жөндөө режими'), {
            'fields': ('maintenance_mode', 'maintenance_message'),
            'description': _('Жөндөө режимин менен сайт жыйнак болот')
        }),
    )
    
    def has_add_permission(self, request):
        return False  # Only one instance should exist
    
    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ('title', 'placement', 'get_is_active', 'order', 'created_at')
    list_filter = ('placement', 'is_active', 'created_at')
    search_fields = ('title', 'description')
    
    fieldsets = (
        (_('Негизги маалымат'), {
            'fields': ('title', 'description', 'image')
        }),
        (_('Ссылка жана орду'), {
            'fields': ('link', 'placement', 'order')
        }),
        (_('Активдүүлүк убактысы'), {
            'fields': ('start_date', 'end_date')
        }),
        (_('Статусу'), {
            'fields': ('is_active',)
        }),
    )
    
    def get_is_active(self, obj):
        is_active = obj.is_active_now
        color = '#009900' if is_active else '#ff0000'
        text = _('Белсүү') if is_active else _('Өчүк')
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            color, text
        )
    get_is_active.short_description = _('Учурдагы статусу')


@admin.register(SEOMetadata)
class SEOMetadataAdmin(admin.ModelAdmin):
    list_display = ('page_title', 'page_url', 'get_meta_title_preview')
    search_fields = ('page_title', 'page_url', 'meta_title')
    
    fieldsets = (
        (_('Бет маалымат'), {
            'fields': ('page_title', 'page_url', 'canonical_url')
        }),
        (_('Meta Tags'), {
            'fields': ('meta_title', 'meta_description', 'meta_keywords')
        }),
        (_('Open Graph'), {
            'fields': ('og_title', 'og_description', 'og_image'),
            'classes': ('collapse',)
        }),
        (_('Twitter Card'), {
            'fields': ('twitter_title', 'twitter_description', 'twitter_image'),
            'classes': ('collapse',)
        }),
        (_('Структурланган маалымат'), {
            'fields': ('structured_data',),
            'classes': ('collapse',)
        }),
    )
    
    def get_meta_title_preview(self, obj):
        return obj.meta_title[:50] + '...' if len(obj.meta_title) > 50 else obj.meta_title
    get_meta_title_preview.short_description = _('Meta Title')


# Customize admin site
admin.site.site_header = _('Муфтияттын Исламий Портали - Админ Панель')
admin.site.site_title = _('Админ Панель')
admin.site.index_title = _('Дамкана')
