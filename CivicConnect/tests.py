import datetime
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from CivicConnect.models import *

# Create your tests here.

class DummyTestCase(TestCase):
    def setUp(self):
        x = 1

    def test_dummy_test_case(self):
        self.assertEqual(1, 1)


class RepresentativesPageTest(TestCase):
    @classmethod
    def setUpTestData(self):
        user = User.objects.create_user(username="testuser1")
        user.set_password('testuser1pass')
        user.save()
        p = User.objects.last().profile
        TemplateSubmission.objects.create(author=p, topic="Test Case", template="Test case template text",
                                          date_posted=datetime.date.today())

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('CivicConnect:representatives'))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/accounts/login/'))

    def test_uses_correct_template(self):
        login = self.client.login(username='testuser1', password='testuser1pass')
        response = self.client.get(reverse('CivicConnect:representatives'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'CivicConnect/representatives.html')


class MyTemplatesTest(TestCase):
    @classmethod
    def setUpTestData(self):
        user = User.objects.create_user(username="testuser1")
        user.set_password('testuser1pass')
        user.save()
        p = User.objects.last().profile
        TemplateSubmission.objects.create(author=p, topic="Test Case", template="Test case template text",
                                          date_posted=datetime.date.today())

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('CivicConnect:mytemplates'))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/accounts/login/'))

    def test_uses_correct_template(self):
        login = self.client.login(username='testuser1', password='testuser1pass')
        response = self.client.get(reverse('CivicConnect:mytemplates'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'CivicConnect/mytemplates.html')



class MyIndexTest(TestCase):
    @classmethod
    def setUpTestData(self):
        user = User.objects.create_user(username="testuser1")
        user.set_password('testuser1pass')
        user.save()
        p = User.objects.last().profile
        TemplateSubmission.objects.create(author=p, topic="Test Case", template="Test case template text",
                                          date_posted=datetime.date.today())

    def test_redirect_to_home_if_not_logged_in(self):
        response = self.client.get(reverse('CivicConnect:index'))
        self.assertRedirects(response, '/CivicConnect/')

    def test_uses_correct_template(self):
        login = self.client.login(username='testuser1', password='testuser1pass')
        response = self.client.get(reverse('CivicConnect:index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'CivicConnect/index.html')


class MyHomeTest(TestCase):
    @classmethod
    def setUpTestData(self):
        user = User.objects.create_user(username="testuser1")
        user.set_password('testuser1pass')
        user.save()
        p = User.objects.last().profile
        TemplateSubmission.objects.create(author=p, topic="Test Case", template="Test case template text",
                                          date_posted=datetime.date.today())

    def test_redirect_to_index_if_logged_in(self):
        login = self.client.login(username='testuser1', password='testuser1pass')
        response = self.client.get(reverse('CivicConnect:home'))
        self.assertRedirects(response, '/CivicConnect/index/')

    def test_uses_correct_template(self):
        response = self.client.get(reverse('CivicConnect:home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'CivicConnect/home.html')