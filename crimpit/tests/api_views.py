from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated

from crimpit.tests.models import CampusTestSet, HangboardTestSet
from crimpit.tests.serializers import TestSetSerializer, ExerciseSerializer


class CampusTestSetApiView(ListCreateAPIView):
    queryset = CampusTestSet.objects.all()
    serializer_class = TestSetSerializer
    permission_classes = [IsAuthenticated]


campus_test_set_api_view = CampusTestSetApiView.as_view()


class HangboardTestSetApiView(ListCreateAPIView):
    queryset = HangboardTestSet.objects.all()
    serializer_class = ExerciseSerializer
    permission_classes = [IsAuthenticated]


hangboard_test_set_api_view = HangboardTestSetApiView.as_view()
