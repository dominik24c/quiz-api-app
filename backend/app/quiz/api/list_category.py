from quiz.models import Category

from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response


class CategoryListView(ListAPIView):
    queryset = Category.objects.all()
    permission_classes = [IsAuthenticated]

    def get(self, request: Request, *args, **kwargs) -> Response:
        categories = Category.objects.values_list('name', flat=True)

        return Response({
            "categories": list(categories)
        })
