from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from django.test import TestCase, Client

from groups.models import Group, GroupMember


def login(client):
    user = User.objects.create(username='Test User', password='Very Secure')

    client.force_login(user)

    return user


def create_group():
    return Group.objects.create(name='Solar City', description='All things solar')


class CreateGroupTest(TestCase):
    def setUp(self):
        self.client = Client()
        login(client=self.client)

    def test_view(self):
        response = self.client.post('/groups/new', {
            'name': 'Mars United',
            'description': 'The United Federation of Mars'
        })

        group = Group.objects.get(name='Mars United')
        self.assertEqual(group.name, 'Mars United')

        self.assertRedirects(response, '/groups/details/' + group.slug)


class ListGroupsTest(TestCase):
    def setUp(self):
        self.group = create_group()
        self.client = Client()

    def test_view(self):
        response = self.client.get('/groups/')

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'groups/group_list.html')


class SingleGroupTest(TestCase):
    def setUp(self):
        self.group = create_group()
        self.client = Client()

    def test_view(self):
        response = self.client.get('/groups/details/' + self.group.slug)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'groups/group_detail.html')


class JoinGroupTest(TestCase):
    def setUp(self):
        self.group = create_group()
        self.client = Client()
        self.user = login(client=self.client)

    def test_view_success(self):
        response = self.client.get('/groups/join/' + self.group.slug)

        self.assertRedirects(response, '/groups/details/' + self.group.slug)

        group_member = GroupMember.objects.get(
            group=self.group, user=self.user)

        self.assertIsNotNone(group_member)
        self.assertEqual(str(list(get_messages(response.wsgi_request))[
            0]), 'You are now a member of the {} group.'.format(self.group.name))

    def test_view_failure(self):
        response = self.client.get('/groups/join/i_dont_exist')

        self.assertEqual(response.status_code, 404)


class LeaveGroupTest(TestCase):
    def setUp(self):
        self.group = create_group()
        self.client = Client()
        self.user = login(client=self.client)
        self.group_member = GroupMember.objects.create(
            group=self.group, user=self.user)

    def test_view_success(self):
        response = self.client.get('/groups/leave/' + self.group.slug)

        self.assertRedirects(response, '/groups/details/' + self.group.slug)
        self.assertEqual(str(list(get_messages(response.wsgi_request))[
            0]), 'You have left the group')

    def test_view_failure(self):
        response = self.client.get('/groups/leave/i_dont_exist')

        self.assertEqual(response.status_code, 302)
        self.assertEqual(str(list(get_messages(response.wsgi_request))[
            0]), 'Sorry you are not in this group')
