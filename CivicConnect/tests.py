import datetime
from django.test import TestCase
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
        Profile.objects.create(user)


class TemplateTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(username="test")
        p = User.objects.last().profile
        TemplateSubmission.objects.create(author=p, topic="Test Case", template="Test case template text",
                                          date_posted=datetime.date.today())

    def test_topic_equal(self):
        template = TemplateSubmission.objects.get(id=1)
        field_label = template._meta.get_field('topic').verbose_name
        self.assertEqual(field_label, 'topic')

    def test_topic_ne(self):
        template = TemplateSubmission.objects.get(id=1)
        field_label = template._meta.get_field('topic').verbose_name
        self.assertNotEqual(field_label, 'template')


