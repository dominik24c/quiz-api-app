from django.contrib.auth.models import User
from django.db import models

from .answer import Answer
from .quiz import Quiz


class Solution(models.Model):
    solved_by = models.ForeignKey(to=User, on_delete=models.CASCADE)
    quiz = models.ForeignKey(to=Quiz, on_delete=models.CASCADE)
    answers = models.ManyToManyField(to=Answer)
    created_at = models.DateTimeField(auto_now_add=True)
