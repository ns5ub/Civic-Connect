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


class YourTestClass(TestCase):
    @classmethod
    def setUpTestData(cls):
        print("setUpTestData: Run once to set up non-modified data for all class methods.")
        pass

    def setUp(self):
        print("setUp: Run once for every test method to setup clean data.")
        pass

    def test_false_is_false(self):
        print("Method: test_false_is_false.")
        self.assertFalse(False)

    def test_one_plus_one_equals_two(self):
        print("Method: test_one_plus_one_equals_two.")
        self.assertEqual(1 + 1, 2)


class ProfileTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        print("setting up")
        user = User.objects.create_user(username="test_user")
        user.set_password("password11")
        user.save()
        p = User.objects.last().profile
        p.bio = "bio"
        p.address = "123 test st"
        p.save()
        print("setup complete")

    def test_bio_eq(self):
        prof = Profile.objects.get(id=1)
        field_label = prof._meta.get_field('bio').verbose_name
        self.assertEqual(field_label, 'bio')
        print("bio test complete")

    def test_eq_to_str(self):
        prof = Profile.objects.get(id=1)
        expected_name = "test_user"
        self.assertEqual(expected_name, str(prof))
        print("to_str complete")

    def test_bio_str(self):
        prof = Profile.objects.get(id=1)
        b = prof.bio
        e_b = "bio"
        self.assertEqual(b, e_b)
        print("bio str complete")

    def test_address_eq(self):
        prof = Profile.objects.get(id=1)
        field_label = prof._meta.get_field('address').verbose_name
        self.assertEqual(field_label, 'address')
        print("address eq complete")

    def test_addy_eq_str(self):
        prof = Profile.objects.get(id=1)
        expected_addy = "123 test st"
        real_addy = prof.address
        self.assertEqual(expected_addy, real_addy)
        print("address str complete")

    def test_prof_auto_update(self):
        prof = Profile.objects.get(id=1)
        prof.bio = "new bio"
        prof.user.save()
        self.assertEqual("new bio", prof.bio)
        self.assertEqual("123 test st", prof.address)
        print("profile auto update complete")




class TemplateTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(username="test")
        p = User.objects.last().profile
        TemplateSubmission.objects.create(author=p, topic="Test Case", template="Test case template text", date_posted=datetime.date.today())

    def test_topic_equal(self): #topic assertEqual
        template = TemplateSubmission.objects.get(id=1)
        field_label = template._meta.get_field('topic').verbose_name
        self.assertEqual(field_label, 'topic')

    def test_topic_ne(self): #topic asserNE
        template = TemplateSubmission.objects.get(id=1)
        field_label = template._meta.get_field('topic').verbose_name
        self.assertNotEqual(field_label, 'template')

    def test_topic_max_length(self): #topic max_length
        template = TemplateSubmission.objects.get(id=1)
        max_length = template._meta.get_field('topic').max_length
        self.assertEqual(max_length, 100)

    def test_template_equal(self): #template assertEqual
        template = TemplateSubmission.objects.get(id=1)
        field_label = template._meta.get_field('template').verbose_name
        self.assertEqual(field_label, 'template')

    def test_template_ne(self): #template assertNE
        template = TemplateSubmission.objects.get(id=1)
        field_label = template._meta.get_field('template').verbose_name
        self.assertNotEqual(field_label, 'topic')

    def test_template_max_length(self):
        template = TemplateSubmission.objects.get(id=1)
        max_length = template._meta.get_field('template').max_length
        self.assertEqual(max_length, 5000)

    # def test_date(self):
    #     template = TemplateSubmission.objects.get(id=1)
    #     field_label = template._meta.get_field('template').DateTimeField
    #     self.assertEqual(field_label, date_posted)

    # class HomepageInstancesByUserListViewTest(TestCase):
    #     def setUp(self):
    #         # Create two users
    #         test_user1 = User.objects.create_user(username='testuser1', password='password')
    #         test_user1.save()
    #
    #         test_bio = Topic.objects.create('bio')
    #
    #
    #     # Check our user is logged in
    #     self.assertEqual(str(response.context['user']), 'testuser1')
    #     # Check that we got a response "success"
    #     self.assertEqual(response.status_code, 200)
    #
    #     # Check we used correct template
    #     self.assertTemplateUsed(response, 'catalog/bookinstance_list_borrowed_user.html')


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


class MyAboutTest(TestCase):
    @classmethod
    def setUpTestData(self):
        user = User.objects.create_user(username="testuser1")
        user.set_password('testuser1pass')
        user.save()
        p = User.objects.last().profile
        TemplateSubmission.objects.create(author=p, topic="Test Case", template="Test case template text",
                                          date_posted=datetime.date.today())

    def test_redirect_to_home_if_not_logged_in(self):
        response = self.client.get(reverse('CivicConnect:about'))
        self.assertRedirects(response, '/CivicConnect/')

    def test_uses_correct_template(self):
        login = self.client.login(username='testuser1', password='testuser1pass')
        response = self.client.get(reverse('CivicConnect:about'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'CivicConnect/about.html')