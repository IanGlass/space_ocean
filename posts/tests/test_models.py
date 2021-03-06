from django.contrib.auth.models import User
from django.utils.text import slugify
from django.urls import reverse

import misaka
import pytest

from posts.models import Post
from groups.models import Group


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
def create_post(create_group):
    global post
    post = Post.objects.create(user=user, group=group, message='Post on this')


@pytest.mark.django_db
class TestPosts():
    def test_string_representation(self, create_post):
        assert str(post) == post.message

    def test_message_html(self, create_post):
        assert post.message_html == misaka.html(post.message)
