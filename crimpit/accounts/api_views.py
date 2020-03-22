from rest_framework.decorators import permission_classes
from rest_framework.generics import ListCreateAPIView, ListAPIView, CreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from crimpit.accounts.models import Athlete, Trainer
from crimpit.accounts.serializers import CustomUserSerializer


class CreateUserApiView(CreateAPIView):
    serializer_class = CustomUserSerializer
    permission_classes = [AllowAny]


create_user_api_view = CreateUserApiView.as_view()


class AthletesList(ListAPIView):
    queryset = Athlete.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = CustomUserSerializer(queryset, many=True)
        return Response(serializer.data)


athletes_list_api_view = AthletesList.as_view()


class TrainersList(AthletesList):
    queryset = Trainer.objects.all()


trainers_list_api_view = TrainersList.as_view()
