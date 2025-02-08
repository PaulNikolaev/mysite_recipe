from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.core.files.storage import default_storage
from .models import Profile


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_delete, sender=Profile)
def delete_profile_avatar(sender, instance, **kwargs):
    if instance.avatar and instance.avatar.name != 'images/avatars/default.png':
        if default_storage.exists(instance.avatar.name):
            default_storage.delete(instance.avatar.name)