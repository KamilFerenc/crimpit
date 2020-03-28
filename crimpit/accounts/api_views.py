from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from crimpit.accounts.models import Athlete, Trainer, CustomUser
from crimpit.accounts.permissions import IsOwnerOrReadOnly
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


class DetailUpdateUserApiView(RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    serializer_class = CustomUserSerializer
    queryset = CustomUser.objects.all()


detail_update_user_api_view = DetailUpdateUserApiView.as_view()
