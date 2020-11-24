import datetime
from django.test import TestCase
from django.utils import timezone
from CivicConnect.models import *
from django.contrib.auth.models import User


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

# class ProfileTest(TestCase):
#     @classmethod
#     def setUpTestData(cls):
#         User.objects.create_user(username="tests")
#         p = User.objects.last().profile
#         Profile.objects.create(user=p, bio="bio", address="address", interests="equality")
#
#     def test_address_equal(self):
#         user = User.objects.get(id=1)
#         max_length = user._meta.get_field('address').max_length
#         self.assertEquals(max_length, 100)

class ProfileTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(username="bears")
        p = User.objects.last()
        Profile.objects.create(user=p, bio="bio", address="123 pee st")

    # def test_bio_equal(self):
    #     prof = Profile.objects.get(id=1)
    #     field_label = prof._meta.get_field('bio').verbose_name
    #     self.assertEqual(field_label, 'bio')

    # def test_bio_ne(self):
    #     profile = Profile.objects.get(id=1)
    #     field_label = profile._meta.get_field('bio').verbose_name
    #     self.assertNotEqual(field_label, 'address')
    #
    # def test_bio_max_length(self):
    #     profile = Profile.objects.get(id=1)
    #     max_length = profile._meta.get_field('bio').max_length
    #     self.assertEqual(max_length, 500)
    #
    # def test_address_equal(self):
    #     profile = Profile.objects.get(id=1)
    #     field_label = profile._meta.get_field('address').verbose_name
    #     self.assertEqual(field_label, 'address')
    #
    # def test_address_ne(self):
    #     profile = Profile.objects.get(id=1)
    #     field_label = profile._meta.get_field('address').verbose_name
    #     self.assertNotEqual(field_label, 'bio')
    #
    # def test_address_max_length(self):
    #     profile = Profile.objects.get(id=1)
    #     max_length = profile._meta.get_field('address').max_length
    #     self.assertEqual(max_length, 100)

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

class UserViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        number_of_authors = 13

    def test_view_url_exists_at_about(self):
        response = self.client.get('/CivicConnect/about/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_exists_at_index(self):
        response = self.client.get('/CivicConnect/index/')
        self.assertEqual(response.status_code, 200)




    # def test_view_uses_correct_template(self):
    #     response = self.client.get(('about'))
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTemplateUsed(response, '/CivicConnect/about/')





