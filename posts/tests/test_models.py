from django.test import TestCase
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.urls import reverse

import misaka

from posts.models import Post
from groups.models import Group


class PostModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            username='Test user', password='test_password')
        self.group = Group.objects.create(
        name='The group', description='The group for everything')
        self.post = Post.objects.create(user=self.user, group=self.group, message='Post on this')

    def test_string_representation(self):
        self.assertEqual(str(self.post), self.post.message)

    def test_slug(self):
        self.assertEqual(self.group.slug, slugify(self.group.name))

    def test_message_html(self):
        self.assertEqual(self.post.message_html,
                         misaka.html(self.post.message))
