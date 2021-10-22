from django.urls import path

from .api import QuizCreateListView, CategoryListView

urlpatterns = [
    path('', QuizCreateListView.as_view(), name='create-list-quiz'),
    path('categories/', CategoryListView.as_view(), name='list-category')
]
