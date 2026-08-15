"""
Views for core app
"""

from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from django_filters.rest_framework import DjangoFilterBackend
from django.utils.translation import gettext_lazy as _
from .models import User, Role, ContactMessage, Category, Tag, Banner, SiteConfiguration
from .serializers import (
    UserSerializer, UserDetailSerializer, UserCreateSerializer, UserUpdateSerializer,
    RoleSerializer, ContactMessageSerializer, ContactMessageDetailSerializer,
    CategorySerializer, TagSerializer, BannerSerializer, SiteConfigurationSerializer
)


class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet for User model
    list: Get all users (paginated)
    retrieve: Get user detail
    create: Register new user
    update: Update user profile
    partial_update: Partial update user profile
    """
    queryset = User.objects.filter(is_active=True)
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['role', 'gender', 'city']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    ordering_fields = ['date_joined', 'username']
    ordering = ['-date_joined']
    
    def get_serializer_class(self):
        if self.action == 'create':
            return UserCreateSerializer
        elif self.action == 'retrieve':
            return UserDetailSerializer
        elif self.action in ['update', 'partial_update']:
            return UserUpdateSerializer
        return UserSerializer
    
    def get_permissions(self):
        if self.action == 'create':
            return [AllowAny()]
        elif self.action in ['update', 'partial_update', 'destroy']:
            return [IsAuthenticated()]
        return [IsAuthenticated()]
    
    def get_queryset(self):
        if self.request.user.is_superuser or self.request.user.is_admin():
            return User.objects.all()
        if self.action == 'list':
            return User.objects.filter(is_active=True, is_public=True)
        return User.objects.filter(id=self.request.user.id)
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def me(self, request):
        """Get current user profile"""
        serializer = UserDetailSerializer(request.user)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def change_password(self, request):
        """Change user password"""
        user = request.user
        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')
        new_password2 = request.data.get('new_password2')
        
        if not user.check_password(old_password):
            return Response(
                {'error': _('Эски пароль туура эмес')},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if new_password != new_password2:
            return Response(
                {'error': _('Жаңы пароль талпыктары дөрөс эмес')},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        user.set_password(new_password)
        user.save()
        return Response({'message': _('Пароль өзгөртүлдү')})
    
    def perform_update(self, serializer):
        """Update user profile"""
        instance = serializer.save()
        # Only allow users to update their own profile
        if self.request.user.id != instance.id and not self.request.user.is_admin():
            instance.refresh_from_db()
            return Response(
                {'error': _('Башка колдонуучунун профилин өзгөртүүгө мүмкүн эмес')},
                status=status.HTTP_403_FORBIDDEN
            )


class RoleViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for Role model (read-only)
    """
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [AllowAny]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'description']


class ContactMessageViewSet(viewsets.ModelViewSet):
    """
    ViewSet for ContactMessage model
    list: Get all messages (admin only)
    create: Submit contact form
    retrieve: Get message detail (admin only)
    """
    queryset = ContactMessage.objects.all()
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['status']
    ordering_fields = ['created_at', 'status']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ContactMessageDetailSerializer
        return ContactMessageSerializer
    
    def get_permissions(self):
        if self.action == 'create':
            return [AllowAny()]
        return [IsAdminUser()]
    
    @action(detail=True, methods=['post'], permission_classes=[IsAdminUser])
    def mark_as_read(self, request, pk=None):
        """Mark message as read"""
        message = self.get_object()
        message.status = 'read'
        message.save()
        return Response({'status': 'marked as read'})
    
    @action(detail=True, methods=['post'], permission_classes=[IsAdminUser])
    def reply(self, request, pk=None):
        """Reply to message"""
        message = self.get_object()
        reply_text = request.data.get('reply')
        
        if not reply_text:
            return Response(
                {'error': _('Жооп текстин киргизиниз')},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        message.reply = reply_text
        message.status = 'replied'
        message.save()
        return Response({'status': 'replied'})


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for Category model (read-only)
    """
    queryset = Category.objects.filter(is_active=True)
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['order', 'name']
    ordering = ['order', 'name']


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for Tag model (read-only)
    """
    queryset = Tag.objects.filter(is_active=True)
    serializer_class = TagSerializer
    permission_classes = [AllowAny]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']
    ordering_fields = ['name']
    ordering = ['name']


class BannerViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for Banner model (read-only)
    """
    queryset = Banner.objects.filter(is_active=True).order_by('placement', 'order')
    serializer_class = BannerSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['placement']


class SiteConfigurationViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for SiteConfiguration model (read-only)
    """
    queryset = SiteConfiguration.objects.all()[:1]
    serializer_class = SiteConfigurationSerializer
    permission_classes = [AllowAny]
    
    def list(self, request, *args, **kwargs):
        """Get site configuration"""
        config = SiteConfiguration.get_instance()
        serializer = self.get_serializer(config)
        return Response(serializer.data)
    
    def retrieve(self, request, *args, **kwargs):
        """Get site configuration"""
        config = SiteConfiguration.get_instance()
        serializer = self.get_serializer(config)
        return Response(serializer.data)


class HealthCheckView(viewsets.ViewSet):
    """
    Health check endpoint for monitoring
    """
    permission_classes = [AllowAny]
    
    @action(detail=False, methods=['get'])
    def check(self, request):
        """Check if API is healthy"""
        return Response({'status': 'healthy'})
