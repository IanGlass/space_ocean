from django.contrib.auth.models import User
from django.contrib.messages import get_messages

import pytest
from pytest_django.asserts import assertTemplateUsed, assertRedirects, assertContains

from groups.models import Group, GroupMember


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
    return Group.objects.create(
        name='Solar City', description='All things solar')


@pytest.mark.django_db
class TestCreateGroup():
    def test_view_success(self, login):
        response = login.post('/groups/new', {
            'name': 'Mars United',
            'description': 'The United Federation of Mars'
        })

        group = Group.objects.get(name='Mars United')
        assert group.name == 'Mars United'

        assertRedirects(response, '/groups/details/' + group.slug)


@pytest.mark.django_db
class TestListGroup():
    def test_view_success(self, client, create_group):
        response = client.get('/groups/')

        assert response.status_code == 200
        assertTemplateUsed(response, 'groups/group_list.html')


@pytest.mark.django_db
class TestSingleGroup():
    def test_view_success(self, client, create_group):
        response = client.get('/groups/details/' + create_group.slug)

        assert response.status_code == 200
        assertTemplateUsed(response, 'groups/group_detail.html')


@pytest.mark.django_db
class TestJoinGroup():
    def test_view_success(self, login, create_group):
        response = login.get('/groups/join/' + create_group.slug)

        assertRedirects(response, '/groups/details/' + create_group.slug)

        group_member = GroupMember.objects.get(
            group=create_group, user=user)

        assert group_member is not None
        assert str(list(get_messages(response.wsgi_request))[
            0]) == 'You are now a member of the {} group.'.format(create_group.name)

    def test_view_failure(self, login, create_group):
        response = login.get('/groups/join/i_dont_exist')

        assert response.status_code == 404


@pytest.mark.django_db
class TestLeaveGroup():
    def test_view_success(self, login, create_group):
        group_member = GroupMember.objects.create(
            group=create_group, user=user)

        response = login.get('/groups/leave/' + create_group.slug)

        assertRedirects(response, '/groups/details/' + create_group.slug)
        assert str(list(get_messages(response.wsgi_request))[
            0]) == 'You have left the group'

    def test_view_failure(self, login, create_group):
        response = login.get('/groups/leave/i_dont_exist')

        assert response.status_code == 302
        assert str(list(get_messages(response.wsgi_request))[
            0]) == 'Sorry you are not in this group'
