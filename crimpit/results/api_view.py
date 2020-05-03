from django.db.models import Q
from rest_framework import status
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView, GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from crimpit.results.models import Result
from crimpit.results.serializers import ResultSerializer


class BaseResultView(GenericAPIView):
    serializer_class = ResultSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Result.objects.filter(
            Q(user=self.request.user)
            | Q(user__pk__in=[self.request.user.athletes.all().values_list('pk', flat=True)]))


class ResultsList(ListCreateAPIView, BaseResultView):
    pass


results_view = ResultsList.as_view()


class ResultDetailView(RetrieveUpdateDestroyAPIView, BaseResultView):
    pass


result_detail = ResultDetailView.as_view()


class StartTestView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ResultSerializer

    def post(self, request):
        serializer = ResultSerializer(data=request.data, context={"request": request})
        if serializer.is_valid(raise_exception=True):
            result = serializer.save()
            return Response(ResultSerializer(result).data, status=status.HTTP_201_CREATED)


start_test = StartTestView.as_view()
