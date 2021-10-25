from django.urls import path

from .api import QuizCreateView, CategoryListView, QuizListView, QuizRetrieveView, SolutionCreateView, UserSolutionsListView

urlpatterns = [
    path('', QuizListView.as_view(), name='list-quiz'),
    path('create/', QuizCreateView.as_view(), name='create-quiz'),
    path('<int:pk>/', QuizRetrieveView.as_view(), name='retrieve-quiz'),
    path('solution/', SolutionCreateView.as_view(), name='create-solution'),
    path('solutions/',UserSolutionsListView.as_view(),name='list-users-solutions'),
    path('categories/', CategoryListView.as_view(), name='list-category')
]
