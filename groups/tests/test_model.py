from django.contrib.auth.models import User
from django.utils.text import slugify
from django.urls import reverse

import misaka
import pytest

from groups.models import Group, GroupMember


@pytest.fixture()
def create_user():
    global user
    user = User.objects.create(username='Test user', password='test_password')


@pytest.fixture()
def create_group(create_user):
    global group
    group = Group.objects.create(
        name='The group', description='The group for everything')


@pytest.fixture()
def create_group_member(create_group):
    global group_member
    group_member = GroupMember.objects.create(user=user, group=group)


@pytest.mark.django_db
class TestGroup():
    def test_group_string_representation(self, create_group):
        assert str(group) == group.name

    def test_group_slug(self, create_group):
        assert group.slug == slugify(group.name)

    def test_group_description_html(self, create_group):
        assert group.description_html == misaka.html(group.description)


@pytest.mark.django_db
class TestGroupMember():
    def test_group_member_string_representation(self, create_group_member):
        assert str(group_member) == user.username
