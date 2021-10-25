from django.contrib.auth.models import User
from quiz.models import Solution
from quiz.serializers import UserSolutionsListSerializer
from rest_framework import generics

from rest_framework.permissions import IsAuthenticated


class UserSolutionsListView(generics.ListAPIView):
    serializer_class = UserSolutionsListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user: User = self.request.user
        return Solution.objects.filter(solved_by=user)
