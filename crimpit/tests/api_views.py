from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from crimpit.tests.permissions import IsCreatorOrReadOnly
from crimpit.tests.models import CampusTestSet, HangboardTestSet, CampusExercise, HangboardExercise, TestSet
from crimpit.tests.serializers import (
    TestSetSerializer, ExerciseSerializer, AddExerciseSerializer, DeleteExerciseSerializer
)


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
    permission_classes = [IsCreatorOrReadOnly]
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
    permission_classes = [IsCreatorOrReadOnly]
    serializer_class = ExerciseSerializer


class CampusExerciseDetailApiView(BaseExerciseDetailView):
    queryset = CampusExercise.objects.all()


campus_exercise_detail = CampusExerciseDetailApiView.as_view()


class HangboardExerciseDetailApiView(BaseExerciseDetailView):
    queryset = HangboardExercise.objects.all()


hangboard_exercise_detail = HangboardExerciseDetailApiView.as_view()


class AddExerciseApiView(UpdateAPIView):
    queryset = TestSet.objects.all()
    permission_classes = [IsCreatorOrReadOnly]
    serializer_class = AddExerciseSerializer

    def get_serializer_context(self):
        context = super(AddExerciseApiView, self).get_serializer_context()
        context.update({
            'test_type': self.get_object().test_type,
        })
        return context

    def patch(self, request, pk):
        serializer = self.serializer_class(instance=self.get_object(),
                                           data=request.data,
                                           context=self.get_serializer_context())
        if serializer.is_valid(raise_exception=True):
            instance = serializer.save()
            return Response(TestSetSerializer(instance).data, status=status.HTTP_200_OK)


add_exercise = AddExerciseApiView.as_view()


class DeleteExerciseApiView(UpdateAPIView):
    queryset = TestSet.objects.all()
    permission_classes = [IsCreatorOrReadOnly]
    serializer_class = DeleteExerciseSerializer

    def patch(self, request, pk):
        serializer = self.serializer_class(instance=self.get_object(), data=request.data)
        if serializer.is_valid(raise_exception=True):
            instance = serializer.save()
            return Response(TestSetSerializer(instance).data, status=status.HTTP_200_OK)


delete_exercise = DeleteExerciseApiView.as_view()
