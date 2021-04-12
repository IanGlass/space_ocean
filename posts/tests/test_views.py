from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from django.test import TestCase, Client

from posts.models import Post
from groups.models import Group


def create_user():
    return User.objects.create(
        username='Leeroy Jenkins', password='Yeet')


def create_group():
    return Group.objects.create(
        name='Post group', description='Post description')


def create_post(group, user):
    return Post.objects.create(
        user=user, group=group, message='Yeah boy')


class PostListTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_view(self):
        response = self.client.get('/posts/')

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'posts/post_list.html')


class UserPostsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = create_user()
        self.group = create_group()
        self.post = create_post(group=self.group, user=self.user)

    def test_view_success(self):
        response = self.client.get('/posts/by/' + self.user.username)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'posts/user_post_list.html')

    def test_view_failure(self):
        response = self.client.get('/posts/by/not_a_chance')

        self.assertEqual(response.status_code, 404)


class PostDetailTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = create_user()
        self.group = create_group()
        self.post = create_post(group=self.group, user=self.user)

    def test_view_success(self):
        response = self.client.get(
            '/posts/by/' + self.user.username + '/' + str(self.post.id))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'posts/post_detail.html')

    def test_view_failure(self):
        response = self.client.get(
            '/posts/by/' + self.user.username + '/not_a_post')

        self.assertEqual(response.status_code, 404)


class CreatePostTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = create_user()
        self.client.force_login(user=self.user)
        self.group = create_group()

    def test_view_success(self):
        response = self.client.post('/posts/new', {
            'group': self.group.id,
            'message': 'The best post in the world'
        })

        self.assertEqual(response.status_code, 302)

        created_post = Post.objects.get(group=self.group)
        self.assertIsNotNone(created_post)


class DeletePostTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = create_user()
        self.client.force_login(user=self.user)
        self.group = create_group()
        self.post = create_post(group=self.group, user=self.user)

    def test_view_success(self):
        response = self.client.delete('/posts/delete/' + str(self.post.id))

        self.assertRedirects(response, '/posts/')
        self.assertEqual(
            str(list(get_messages(response.wsgi_request))[0]), 'Post Deleted')
