from django.contrib.auth.models import User
from django.utils.text import slugify
from django.urls import reverse

import misaka
import pytest

from groups.models import Group, GroupMember


@pytest.mark.django_db
@pytest.fixture()
def create_user():
    global user
    user = User.objects.create(username='Test user', password='test_password')


@pytest.mark.django_db
@pytest.fixture()
def create_group(create_user):
    global group
    group = Group.objects.create(
        name='The group', description='The group for everything')


@pytest.mark.django_db
@pytest.fixture()
def create_group_member(create_group):
    global group_member
    group_member = GroupMember.objects.create(user=user, group=group)


@pytest.mark.django_db
def test_group_string_representation(create_group):
    assert str(group) == group.name


@pytest.mark.django_db
def test_group_slug(create_group):
    assert group.slug == slugify(group.name)


@pytest.mark.django_db
def test_group_description_html(create_group):
    assert group.description_html == misaka.html(group.description)


@pytest.mark.django_db
def test_group_member_string_representation(create_group_member):
    assert str(group_member) == user.username
