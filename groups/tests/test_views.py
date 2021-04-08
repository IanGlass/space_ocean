from django.contrib.auth.models import User
from django.contrib.messages import get_messages

import pytest

from groups.models import Group, GroupMember
from groups.views import CreateGroup


@pytest.fixture(autouse=True)
def create_user():
    global user
    user = User.objects.create(username='Test User', password='Very Secure')


@pytest.fixture()
def create_group():
    yield Group.objects.create(name='Solar City', description='All topics solar')

    Group.objects.get(name='Solar City').delete()


@pytest.fixture()
def login(client):
    client.force_login(user)
    yield client

    User.objects.get(username=user.username).delete()


@pytest.mark.django_db
def test_list_groups(client):
    response = client.get('/groups/')
    assert response.status_code == 200


@pytest.mark.django_db
def test_single_group(client, create_group):
    response = client.get('/groups/details/' + create_group.slug)
    assert response.status_code == 200


@pytest.mark.django_db
def test_create_group(login):
    response = login.post('/groups/new/', {
        'name': 'Mars United',
        'description': 'The United Federation of Mars'
    })

    assert response.status_code == 302

    created_group = Group.objects.get(name='Mars United')
    assert created_group.name == 'Mars United'


@pytest.mark.django_db
def test_join_group_success(login, create_group):
    response = login.get('/groups/join/' + create_group.slug)

    assert response.status_code == 302
    assert str(list(get_messages(response.wsgi_request))[
               0]) == 'You are now a member of the {} group.'.format(create_group.name), 'Incorrect flash message'

    created_group_member = GroupMember.objects.get(user=user)
    assert created_group_member is not None


@pytest.mark.django_db
def test_join_group_failure(login, create_group):
    response = login.get('/groups/join/i_dont_exist')

    assert response.status_code == 404
