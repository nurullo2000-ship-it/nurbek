"""
Core application models
Foundation models for the Islamic portal
"""

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone


class BaseModel(models.Model):
    """
    Abstract base model with common fields for all models
    """
    created_at = models.DateTimeField(_('Түзүлгөн убакыт'), auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(_('Жаңыланган убакыт'), auto_now=True)
    is_active = models.BooleanField(_('Белсүү'), default=True, db_index=True)

    class Meta:
        abstract = True
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.__class__.__name__} - {getattr(self, 'name', self.pk)}"


class Role(models.Model):
    """
    User roles for permission management
    
    Roles:
    - SUPERADMIN: Full system access
    - ADMIN: Administrative access
    - EDITOR: Can create/edit content
    - MODERATOR: Can moderate content
    - SCHOLAR: Can answer religious questions
    - USER: Regular user (read-only)
    """
    SUPERADMIN = 'superadmin'
    ADMIN = 'admin'
    EDITOR = 'editor'
    MODERATOR = 'moderator'
    SCHOLAR = 'scholar'
    USER = 'user'

    ROLE_CHOICES = [
        (SUPERADMIN, _('Суперадмин')),
        (ADMIN, _('Администратор')),
        (EDITOR, _('Редактор')),
        (MODERATOR, _('Модератор')),
        (SCHOLAR, _('Аалым')),
        (USER, _('Пайдалануучу')),
    ]

    name = models.CharField(_('Аталышы'), max_length=50, unique=True, choices=ROLE_CHOICES)
    description = models.TextField(_('Сыпаттамасы'), blank=True)
    permissions = models.ManyToManyField(
        'auth.Permission',
        blank=True,
        verbose_name=_('Өндүрүшүнүн мээстери')
    )
    created_at = models.DateTimeField(_('Түзүлгөн убакыт'), auto_now_add=True)

    class Meta:
        verbose_name = _('Роль')
        verbose_name_plural = _('Рольдор')
        ordering = ['name']

    def __str__(self):
        return f"{self.get_name_display()}"


class User(AbstractUser, BaseModel):
    """
    Custom user model with role-based access control
    """
    GENDER_CHOICES = [
        ('M', _('Эркек')),
        ('F', _('Аял')),
        ('O', _('Башка')),
    ]

    email = models.EmailField(_('Email адреси'), unique=True)
    phone_number = models.CharField(_('Телефон номери'), max_length=20, blank=True)
    avatar = models.ImageField(_('Сүрөт'), upload_to='avatars/%Y/%m/%d/', null=True, blank=True)
    bio = models.TextField(_('Биография'), blank=True, max_length=500)
    gender = models.CharField(_('Жынысы'), max_length=1, choices=GENDER_CHOICES, blank=True)
    birth_date = models.DateField(_('Төрөлгөн күнү'), null=True, blank=True)
    
    # Location info
    city = models.CharField(_('Шаар'), max_length=100, blank=True)
    country = models.CharField(_('Өлкө'), max_length=100, default='Кыргызстан')
    
    # Social links
    website = models.URLField(_('Веб-сайт'), blank=True)
    social_id = models.CharField(_('Социалдык сеть ID'), max_length=255, blank=True)
    
    # Role
    role = models.ForeignKey(Role, on_delete=models.PROTECT, verbose_name=_('Роль'), null=True, blank=True)
    
    # Status
    email_verified = models.BooleanField(_('Email текшерилген'), default=False)
    phone_verified = models.BooleanField(_('Телефон текшерилген'), default=False)
    
    # Privacy
    is_public = models.BooleanField(_('Жарыя профили'), default=True)
    newsletter = models.BooleanField(_('Newsletter-ге жазылуу'), default=True)
    
    class Meta:
        verbose_name = _('Пайдалануучу')
        verbose_name_plural = _('Пайдалануучулар')
        ordering = ['-date_joined']
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['username']),
            models.Index(fields=['role']),
            models.Index(fields=['is_active']),
        ]

    def __str__(self):
        return f"{self.get_full_name() or self.username}"

    def get_role_name(self):
        """Get role name"""
        if self.role:
            return self.role.get_name_display()
        return _('Пайдалануучу')

    def is_superadmin(self):
        """Check if user is superadmin"""
        return self.role and self.role.name == Role.SUPERADMIN

    def is_admin(self):
        """Check if user is admin or above"""
        return self.role and self.role.name in [Role.SUPERADMIN, Role.ADMIN]

    def is_editor(self):
        """Check if user can edit content"""
        return self.role and self.role.name in [Role.SUPERADMIN, Role.ADMIN, Role.EDITOR]

    def is_scholar(self):
        """Check if user is a scholar"""
        return self.role and self.role.name == Role.SCHOLAR


class ContactMessage(BaseModel):
    """
    Contact form submissions
    """
    STATUS_CHOICES = [
        ('new', _('Жаңы')),
        ('read', _('Окулган')),
        ('replied', _('Жооп берилген')),
        ('closed', _('Жабык')),
    ]

    name = models.CharField(_('Аталышы'), max_length=200)
    email = models.EmailField(_('Email'))
    phone = models.CharField(_('Телефон'), max_length=20, blank=True)
    subject = models.CharField(_('Тема'), max_length=300)
    message = models.TextField(_('Билдирүү'))
    status = models.CharField(_('Статусу'), max_length=20, choices=STATUS_CHOICES, default='new')
    reply = models.TextField(_('Жооп'), blank=True)
    
    class Meta:
        verbose_name = _('Байланыш билдирүүсү')
        verbose_name_plural = _('Байланыш билдирүүлөрү')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status', '-created_at']),
            models.Index(fields=['email']),
        ]

    def __str__(self):
        return f"{self.subject} - {self.name}"


class Category(BaseModel):
    """
    Content categories (for news, articles, etc.)
    """
    name = models.CharField(_('Аталышы'), max_length=200, unique=True)
    slug = models.SlugField(_('URL'), unique=True, max_length=200)
    description = models.TextField(_('Сыпаттамасы'), blank=True)
    icon = models.CharField(_('Икона'), max_length=50, blank=True, help_text='Font Awesome icon class')
    color = models.CharField(_('Түсү'), max_length=7, default='#000000', help_text='Hex color code')
    order = models.PositiveIntegerField(_('Сорту'), default=0)
    
    class Meta:
        verbose_name = _('Категория')
        verbose_name_plural = _('Категориялар')
        ordering = ['order', 'name']
        indexes = [
            models.Index(fields=['slug']),
        ]

    def __str__(self):
        return self.name


class Tag(BaseModel):
    """
    Tags for content organization
    """
    name = models.CharField(_('Аталышы'), max_length=100, unique=True)
    slug = models.SlugField(_('URL'), unique=True)
    
    class Meta:
        verbose_name = _('Тег')
        verbose_name_plural = _('Тегдер')
        ordering = ['name']
        indexes = [
            models.Index(fields=['slug']),
        ]

    def __str__(self):
        return self.name


class SiteConfiguration(BaseModel):
    """
    Global site configuration
    """
    site_title = models.CharField(_('Сайттын аталышы'), max_length=255, default='Муфтияттын Исламий Портали')
    site_description = models.TextField(_('Сайттын сыпаттамасы'), default='Кыргызстандагы исламий маалымат порталы')
    site_logo = models.ImageField(_('Логосу'), upload_to='config/', null=True, blank=True)
    site_icon = models.ImageField(_('Сайт икона'), upload_to='config/', null=True, blank=True)
    
    # Contact info
    phone = models.CharField(_('Телефон'), max_length=20, blank=True)
    email = models.EmailField(_('Email'), blank=True)
    address = models.TextField(_('Дареги'), blank=True)
    
    # Social media
    facebook_url = models.URLField(_('Facebook'), blank=True)
    twitter_url = models.URLField(_('Twitter'), blank=True)
    instagram_url = models.URLField(_('Instagram'), blank=True)
    youtube_url = models.URLField(_('YouTube'), blank=True)
    telegram_url = models.URLField(_('Telegram'), blank=True)
    
    # Settings
    maintenance_mode = models.BooleanField(_('Жөндөө режими'), default=False)
    maintenance_message = models.TextField(_('Жөндөө билдирүүсү'), blank=True)
    
    google_analytics_id = models.CharField(_('Google Analytics ID'), max_length=50, blank=True)
    google_maps_api_key = models.CharField(_('Google Maps API ачы'), max_length=255, blank=True)
    
    class Meta:
        verbose_name = _('Сайт конфигурациясы')
        verbose_name_plural = _('Сайт конфигурациялары')

    def __str__(self):
        return self.site_title

    def save(self, *args, **kwargs):
        # Ensure only one instance exists
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def get_instance(cls):
        """Get or create the singleton instance"""
        instance, _ = cls.objects.get_or_create(pk=1)
        return instance


class Banner(BaseModel):
    """
    Website banners/sliders
    """
    PLACEMENT_CHOICES = [
        ('homepage', _('Башкы бет')),
        ('sidebar', _('Каптал панели')),
        ('top', _('Өңү жакын')),
        ('bottom', _('Төмөнү жакын')),
    ]

    title = models.CharField(_('Аталышы'), max_length=255)
    description = models.TextField(_('Сыпаттамасы'), blank=True)
    image = models.ImageField(_('Сүрөт'), upload_to='banners/%Y/%m/')
    link = models.URLField(_('Сылтама'), blank=True)
    placement = models.CharField(_('Орду'), max_length=20, choices=PLACEMENT_CHOICES, default='homepage')
    order = models.PositiveIntegerField(_('Сорту'), default=0)
    start_date = models.DateTimeField(_('Баштоо убакыты'), null=True, blank=True)
    end_date = models.DateTimeField(_('Аяктоо убакыты'), null=True, blank=True)
    
    class Meta:
        verbose_name = _('Баннер')
        verbose_name_plural = _('Баннерлер')
        ordering = ['placement', 'order', '-created_at']

    def __str__(self):
        return self.title

    @property
    def is_active_now(self):
        """Check if banner is active now"""
        now = timezone.now()
        start_ok = not self.start_date or self.start_date <= now
        end_ok = not self.end_date or self.end_date >= now
        return self.is_active and start_ok and end_ok


class SEOMetadata(models.Model):
    """
    SEO metadata for pages
    """
    page_title = models.CharField(_('Бет аталышы'), max_length=255, unique=True)
    page_url = models.SlugField(_('Бет URL'), unique=True)
    meta_title = models.CharField(_('Meta Title'), max_length=255)
    meta_description = models.CharField(_('Meta Description'), max_length=160)
    meta_keywords = models.CharField(_('Meta Keywords'), max_length=255, blank=True)
    canonical_url = models.URLField(_('Canonical URL'), blank=True)
    
    # Open Graph
    og_title = models.CharField(_('OG Title'), max_length=255, blank=True)
    og_description = models.CharField(_('OG Description'), max_length=160, blank=True)
    og_image = models.ImageField(_('OG Image'), upload_to='seo/', blank=True)
    
    # Twitter
    twitter_title = models.CharField(_('Twitter Title'), max_length=255, blank=True)
    twitter_description = models.CharField(_('Twitter Description'), max_length=160, blank=True)
    twitter_image = models.ImageField(_('Twitter Image'), upload_to='seo/', blank=True)
    
    # Structured data
    structured_data = models.JSONField(_('Структурланган маалымат'), blank=True, null=True)
    
    created_at = models.DateTimeField(_('Түзүлгөн убакыт'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Жаңыланган убакыт'), auto_now=True)

    class Meta:
        verbose_name = _('SEO Metadata')
        verbose_name_plural = _('SEO Metadatalar')

    def __str__(self):
        return self.page_title
