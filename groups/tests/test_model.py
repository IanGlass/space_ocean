from django.test import TestCase
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.urls import reverse

import misaka

from groups.models import Group, GroupMember


def create_group():
    return Group.objects.create(
        name='The group', description='The group for everything')


class GroupModelTest(TestCase):
    def setUp(self):
        self.group = create_group()

    def test_string_representation(self):
        self.assertEqual(str(self.group), self.group.name)

    def test_slug(self):
        self.assertEqual(self.group.slug, slugify(self.group.name))

    def test_description_html(self):
        self.assertEqual(self.group.description_html,
                         misaka.html(self.group.description))


class GroupMemberTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            username='Test user', password='test_password')
        self.group = create_group()
        self.group_member = GroupMember.objects.create(user=self.user, group=self.group)

    def test_string_representation(self):
      self.assertEqual(str(self.group_member), self.user.username)
