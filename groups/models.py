from django.db.models import Model, CharField, SlugField, TextField, ManyToManyField, ForeignKey, CASCADE
from django.utils.text import slugify
from django.contrib.auth import get_user_model
from django.urls import reverse
from django import template

import misaka

# register = template.library()

User = get_user_model()

class Group(Model):
    name = CharField(max_length=255, unique=True)
    slug = SlugField(allow_unicode=True, unique=True)
    description = TextField(blank=True, default='')
    description_html = TextField(editable=False, default='', blank=True)
    members = ManyToManyField(User, through='GroupMember')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        self.description_html = misaka.html(self.description)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('groups:single', kwargs={'slug': self.slug})

    class Meta:
        ordering = ['name']


class GroupMember(Model):
    group = ForeignKey(Group, related_name='memberships', on_delete=CASCADE)
    user = ForeignKey(User, related_name='user_groups', on_delete=CASCADE)

    def __str__(self):
        return self.user.username

    class Meta:
        unique_together = ('group', 'user')
