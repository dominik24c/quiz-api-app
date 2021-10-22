from django.db import models

from .question import Question


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.CharField(max_length=150)
    is_correct = models.BooleanField()
