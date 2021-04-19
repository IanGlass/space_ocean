from django.contrib.messages import get_messages

import pytest
from pytest_django.asserts import assertTemplateUsed, assertRedirects

from posts.models import Post
from groups.models import Group


@pytest.fixture(autouse=True)
def create_user(django_user_model):
    global user
    user = django_user_model.objects.create(username='Leeroy Jenkins', password='yeet')


@pytest.fixture()
def login(client):
    client.force_login(user)

    return client


@pytest.fixture()
def create_group():
    return Group.objects.create(name='Solar City', description='All things solar')


@pytest.mark.django_db
def create_post(group):
    return Post.objects.create(
        user=user, group=group, message='Yeah boy')


@pytest.mark.django_db
class TestPostList():
    def test_view_success(self, client):
        response = client.get('/posts/')

        assert response.status_code == 200
        assertTemplateUsed(response, 'posts/post_list.html')


@pytest.mark.django_db
class TestUserPosts():
    def test_view_success(self, login, create_group):
        post = create_post(group=create_group)
        response = login.get('/posts/by/' + user.username)

        assert response.status_code == 200
        assertTemplateUsed(response, 'posts/user_post_list.html')

    def test_view_failure(self, login, create_group):
        response = login.get('/posts/by/not_a_chance')

        assert response.status_code == 404


@pytest.mark.django_db
class TestPostDetail():
    def test_view_success(self, login, create_group):
        post = create_post(group=create_group)
        response = login.get('/posts/by/' + user.username + '/' + str(post.id))

        assert response.status_code == 200
        assertTemplateUsed(response, 'posts/post_detail.html')

    def test_view_failure(self, login, create_group):
        post = create_post(group=create_group)
        response = login.get('/posts/by/' + user.username + '/not_a_post')

        assert response.status_code == 404


@pytest.mark.django_db
class TestCreatePost():
    def test_view_success(self, login, create_group):
        response = login.post('/posts/new', {
            'group': create_group.id,
            'message': 'The best post in the world'
        })

        assert response.status_code == 302

        created_post = Post.objects.get(group=create_group)
        assert created_post is not None


@pytest.mark.django_db
class TestDeletePost():
    def test_delete_post(self, login, create_group):
        post = create_post(group=create_group)
        response = login.delete('/posts/delete/' + str(post.id))

        assertRedirects(response, '/posts/')
        assert str(list(get_messages(response.wsgi_request))
                   [0]) == 'Post Deleted'
