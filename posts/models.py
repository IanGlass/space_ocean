from django.db.models import Model, ForeignKey, DateTimeField, TextField, ForeignKey, CASCADE
from django.urls import reverse
from django.conf import settings
from django.contrib.auth import get_user_model

import misaka

from groups.models import Group

User = get_user_model()


class Post(Model):
    user = ForeignKey(User, related_name='posts', on_delete=CASCADE)
    created_at = DateTimeField(auto_now=True)
    message = TextField()
    message_html = TextField(editable=False)
    group = ForeignKey(
        Group, related_name='posts', null=True, blank=True, on_delete=CASCADE)

    def __str__(self):
        return self.message

    def save(self, *args, **kwargs):
        self.message_html = misaka.html(self.message)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('posts:single', kwargs={'username': self.user.username, 'pk': self.pk})

    class Meta:
        ordering = ['-created_at']
        unique_together = ['user', 'message']
