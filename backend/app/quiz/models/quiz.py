from django.db import models
from django.contrib.auth.models import User

from .category import Category


class Quiz(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.RESTRICT)
    title = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['title'])
        ]