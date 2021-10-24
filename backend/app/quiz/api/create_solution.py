from quiz.models import Solution
from quiz.serializers import SolutionCreateSerializer

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response


class SolutionCreateView(generics.CreateAPIView):
    serializer_class = SolutionCreateSerializer
    queryset = Solution.objects.all()

    permission_classes = [IsAuthenticated]

    def post(self, request: Request, *args, **kwargs) -> Response:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({
            "message": "Solution was saved!"
        })
