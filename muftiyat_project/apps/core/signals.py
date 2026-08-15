"""Create a few safe defaults after the core app is migrated."""
from django.db.models.signals import post_migrate
from django.dispatch import receiver

from .models import Role, SiteConfiguration


@receiver(post_migrate)
def create_defaults(sender, **kwargs):
    if sender.name != "apps.core":
        return

    for name in [Role.SUPERADMIN, Role.ADMIN, Role.EDITOR, Role.MODERATOR, Role.SCHOLAR, Role.USER]:
        Role.objects.get_or_create(name=name)

    SiteConfiguration.objects.get_or_create(
        pk=1,
        defaults={
            "site_title": "Муфтият Кыргызстан",
            "site_description": "Кыргызстан мусулмандары үчүн расмий маалымат порталы.",
        },
    )
