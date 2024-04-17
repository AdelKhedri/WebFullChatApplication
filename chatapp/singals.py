from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from .models import GroupChat
from uuid import uuid4


def create_uuid_unique(new_uuid=None):
    if not new_uuid:
     uuid = uuid4().hex[:20]
    if GroupChat.objects.filter(address=uuid).exists():
        uuid = uuid4().hex[:20]
        create_uuid_unique(uuid)
    return uuid

@receiver(post_save, sender=GroupChat)
def add_manager(sender, instance, **kwargs):
    instance.address = create_uuid_unique()