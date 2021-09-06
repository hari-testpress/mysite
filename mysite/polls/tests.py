from django.test import TestCase
from .models import Question
from django.utils import timezone
import datetime

# Create your tests here.


class TestQuestionModel(TestCase):
    def test_was_published_recently_should_return_false_for_question_older_than_a_day(
        self,
    ):
        time = timezone.now() - datetime.timedelta(days=2)
        old_question = Question(pub_date=time)
        self.assertFalse(old_question.was_published_recently())

    def test_was_published_recently_with_future_question(self):
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertFalse(future_question.was_published_recently())

    def test_was_published_recently_should_return_true_for_question_created_within_day(
        self,
    ):
        present_question = Question(
            question_text="2+2", pub_date=timezone.now()
        )
        self.assertTrue(present_question.was_published_recently())
