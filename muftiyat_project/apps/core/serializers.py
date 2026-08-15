"""
Serializers for core app
"""

from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field
from django.contrib.auth.password_validation import validate_password
from django.utils.translation import gettext_lazy as _
from .models import User, Role, ContactMessage, Category, Tag, Banner, SiteConfiguration


class RoleSerializer(serializers.ModelSerializer):
    """Serializer for Role model"""
    permissions_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Role
        fields = ['id', 'name', 'description', 'permissions_count']
        read_only_fields = ['id']
    
    @extend_schema_field(serializers.IntegerField())
    def get_permissions_count(self, obj) -> int:
        return obj.permissions.count()


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model"""
    role = RoleSerializer(read_only=True)
    full_name = serializers.CharField(source='get_full_name', read_only=True)
    
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name', 'full_name',
            'phone_number', 'avatar', 'bio', 'gender', 'birth_date',
            'city', 'country', 'website', 'role', 'is_public',
            'email_verified', 'phone_verified', 'date_joined', 'created_at'
        ]
        read_only_fields = ['id', 'date_joined', 'created_at']


class UserDetailSerializer(UserSerializer):
    """Detailed serializer for User model"""
    class Meta(UserSerializer.Meta):
        fields = UserSerializer.Meta.fields + [
            'newsletter', 'is_active', 'last_login', 'updated_at'
        ]
        read_only_fields = UserSerializer.Meta.read_only_fields + ['last_login', 'updated_at']


class UserCreateSerializer(serializers.ModelSerializer):
    """Serializer for user registration"""
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True, label=_('Пароль дұрыс'))

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2', 'first_name', 'last_name']

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {"password": _("Пароль талпыктары дөрөс эмес.")}
            )
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
        # Assign default role
        default_role = Role.objects.filter(name=Role.USER).first()
        if default_role:
            user.role = default_role
            user.save()
        return user


class UserUpdateSerializer(serializers.ModelSerializer):
    """Serializer for user profile update"""
    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'phone_number', 'avatar', 'bio',
            'gender', 'birth_date', 'city', 'country', 'website', 'is_public'
        ]


class ContactMessageSerializer(serializers.ModelSerializer):
    """Serializer for ContactMessage model"""
    class Meta:
        model = ContactMessage
        fields = ['id', 'name', 'email', 'phone', 'subject', 'message', 'status', 'created_at']
        read_only_fields = ['id', 'status', 'created_at']


class ContactMessageDetailSerializer(ContactMessageSerializer):
    """Detailed serializer for ContactMessage"""
    class Meta(ContactMessageSerializer.Meta):
        fields = ContactMessageSerializer.Meta.fields + ['reply', 'updated_at']


class CategorySerializer(serializers.ModelSerializer):
    """Serializer for Category model"""
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description', 'icon', 'color', 'order', 'is_active']
        read_only_fields = ['id']


class TagSerializer(serializers.ModelSerializer):
    """Serializer for Tag model"""
    class Meta:
        model = Tag
        fields = ['id', 'name', 'slug', 'is_active']
        read_only_fields = ['id']


class BannerSerializer(serializers.ModelSerializer):
    """Serializer for Banner model"""
    is_active_now = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = Banner
        fields = [
            'id', 'title', 'description', 'image', 'link', 'placement',
            'order', 'start_date', 'end_date', 'is_active', 'is_active_now', 'created_at'
        ]
        read_only_fields = ['id', 'is_active_now', 'created_at']


class SiteConfigurationSerializer(serializers.ModelSerializer):
    """Serializer for SiteConfiguration model"""
    class Meta:
        model = SiteConfiguration
        fields = [
            'site_title', 'site_description', 'site_logo', 'site_icon',
            'phone', 'email', 'address', 'facebook_url', 'twitter_url',
            'instagram_url', 'youtube_url', 'telegram_url',
            'maintenance_mode', 'maintenance_message'
        ]
        read_only_fields = [
            'site_logo', 'site_icon'  # Only admins can upload
        ]


class HealthStatusSerializer(serializers.Serializer):
    """Response returned by the API health endpoints."""
    status = serializers.CharField()
    service = serializers.CharField(required=False)
