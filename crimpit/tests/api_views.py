from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated

from crimpit.accounts.permissions import IsOwnerOrReadOnly
from crimpit.tests.models import CampusTestSet, HangboardTestSet, CampusExercise, HangboardExercise
from crimpit.tests.serializers import TestSetSerializer, ExerciseSerializer


class BaseTestSetApiView(ListCreateAPIView):
    serializer_class = TestSetSerializer
    permission_classes = [IsAuthenticated]


class CampusTestSetApiView(BaseTestSetApiView):
    queryset = CampusTestSet.objects.all()


campus_test_set = CampusTestSetApiView.as_view()


class HangboardTestSetApiView(BaseTestSetApiView):
    queryset = HangboardTestSet.objects.all()


hangboard_test_set = HangboardTestSetApiView.as_view()


class BaseTestSetDetailView(RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    serializer_class = TestSetSerializer


class CampusTestSetDetailApiView(BaseTestSetDetailView):
    queryset = CampusTestSet.objects.all()


campus_test_set_detail = CampusTestSetDetailApiView.as_view()


class HangboardTestSetDetailApiView(BaseTestSetDetailView):
    queryset = HangboardTestSet.objects.all()


hangboard_test_set_detail = HangboardTestSetDetailApiView.as_view()


class BaseExerciseApiView(ListCreateAPIView):
    serializer_class = ExerciseSerializer
    permission_classes = [IsAuthenticated]


class CampusExerciseApiView(BaseExerciseApiView):
    queryset = CampusExercise.objects.all()


campus_exercise = CampusExerciseApiView.as_view()


class HangboardExerciseApiView(BaseExerciseApiView):
    queryset = HangboardExercise.objects.all()


hangboard_exercise = HangboardExerciseApiView.as_view()


class BaseExerciseDetailView(RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    serializer_class = ExerciseSerializer


class CampusExerciseDetailApiView(BaseExerciseDetailView):
    queryset = CampusExercise.objects.all()


campus_exercise_detail = CampusExerciseDetailApiView.as_view()


class HangboardExerciseDetailApiView(BaseExerciseDetailView):
    queryset = HangboardExercise.objects.all()


hangboard_exercise_detail = HangboardExerciseDetailApiView.as_view()
