from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from crimpit.accounts.models import Athlete, Trainer
from crimpit.accounts.serializers import CustomUserSerializer


class AthletesList(ListCreateAPIView):
    queryset = Athlete.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [AllowAny]

    def list(self, request):
        queryset = self.get_queryset()
        serializer = CustomUserSerializer(queryset, many=True)
        return Response(serializer.data)


athletes_list_api_view = AthletesList.as_view()


class TrainersList(AthletesList):
    queryset = Trainer.objects.all()


trainers_list_api_view = TrainersList.as_view()
