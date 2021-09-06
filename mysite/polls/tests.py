from django.test import TestCase
from .models import Question
from django.utils import timezone
from django.urls import reverse
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


def create_question(question_text, days):
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)


class QuestionIndexViewTests(TestCase):
    def test_should_display_no_polls_are_available_if_no_questions_exist(self):
        response = self.client.get(reverse("polls:index"))
        self.assertContains(response, "No polls are available.")

    def test_should_display_questions_published_in_the_past(self):
        question = create_question(question_text="Past question.", days=-30)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(
            response.context["latest_question_list"],
            [question],
            transform=lambda x: x,
        )

    def test_should_not_display_future_question(self):
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse("polls:index"))
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context["latest_question_list"], [])

    def test_with_past_and_future_question_should_display_only_past_question(
        self,
    ):
        question = create_question(question_text="Past question.", days=-30)
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(
            response.context["latest_question_list"],
            [question],
            transform=lambda x: x,
        )
