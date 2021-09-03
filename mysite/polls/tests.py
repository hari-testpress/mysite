from django.test import TestCase
from .models import Question
from django.utils import timezone
import datetime

# Create your tests here.


class TestQuestionModel(TestCase):
    def test_was_published_recently_with_future_question(self):
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(question_text="whats up", pub_date=time)
        self.assertFalse(future_question.was_published_recently)

    def test_was_published_recently_with_old_question(self):
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertFalse(old_question.was_published_recently)

    def test_was_published_recently_with_present_question(self):
        present_question = Question(
            question_text="2+2", pub_date=timezone.now()
        )
        self.assertTrue(present_question.was_published_recently)
