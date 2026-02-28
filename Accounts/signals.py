from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User

@receiver(post_save, sender=User)
def set_default_role(sender, instance, created, **kwargs):
    if created and not instance.role:
        if User.objects.count() == 1:
            instance.role = 'ADMIN'
        else:
            instance.role = 'MEMBER'
        instance.save()