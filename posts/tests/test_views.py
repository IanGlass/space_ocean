from django.contrib.auth.models import User
from django.contrib.messages import get_messages

import pytest
from pytest_django.asserts import assertTemplateUsed, assertRedirects

from posts.models import Post
from groups.models import Group


@pytest.fixture(autouse=True)
def create_user():
    global user
    user = User.objects.create(username='Leeroy Jenkins', password='yeet')


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
def test_post_list(client):
    response = client.get('/posts/')

    assert response.status_code == 200
    assertTemplateUsed(response, 'posts/post_list.html')


@pytest.mark.django_db
def test_user_post_success(login, create_group):
    post = create_post(group=create_group)
    response = login.get('/posts/by/' + user.username)

    assert response.status_code == 200
    assertTemplateUsed(response, 'posts/user_post_list.html')


@pytest.mark.django_db
def test_user_post_failure(login, create_group):
    response = login.get('/posts/by/not_a_chance')

    assert response.status_code == 404


@pytest.mark.django_db
def test_post_detail_success(login, create_group):
    post = create_post(group=create_group)
    response = login.get('/posts/by/' + user.username + '/' + str(post.id))

    assert response.status_code == 200
    assertTemplateUsed(response, 'posts/post_detail.html')


@pytest.mark.django_db
def test_post_detail_failure(login, create_group):
    post = create_post(group=create_group)
    response = login.get('/posts/by/' + user.username + '/not_a_post')

    assert response.status_code == 404


@pytest.mark.django_db
def test_create_post(login, create_group):
    response = login.post('/posts/new', {
        'group': create_group.id,
        'message': 'The best post in the world'
    })

    assert response.status_code == 302

    created_post = Post.objects.get(group=create_group)
    assert created_post is not None


@pytest.mark.django_db
def test_delete_post(login, create_group):
    post = create_post(group=create_group)
    response = login.delete('/posts/delete/' + str(post.id))

    assertRedirects(response, '/posts/')
    assert str(list(get_messages(response.wsgi_request))[0]) == 'Post Deleted'
