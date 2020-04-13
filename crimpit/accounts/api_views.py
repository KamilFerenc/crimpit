from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveUpdateAPIView, UpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated

from crimpit.accounts.models import Athlete, Trainer, CustomUser
from crimpit.accounts.permissions import IsOwnerOrReadOnly
from crimpit.accounts.serializers import CustomUserSerializer, AddTestSerializer, DeleteTestSerializer


class CreateUserApiView(CreateAPIView):
    serializer_class = CustomUserSerializer
    permission_classes = [AllowAny]


create_user_api_view = CreateUserApiView.as_view()


class AthletesList(ListAPIView):
    queryset = Athlete.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated]


athletes_list_api_view = AthletesList.as_view()


class TrainersList(AthletesList):
    queryset = Trainer.objects.all()


trainers_list_api_view = TrainersList.as_view()


class DetailUpdateUserApiView(RetrieveUpdateAPIView):
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = CustomUserSerializer
    queryset = CustomUser.objects.all()


detail_update_user_api_view = DetailUpdateUserApiView.as_view()


class AddTestApiView(UpdateAPIView):
    serializer_class = AddTestSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get_object(self):
        return self.request.user


add_test = AddTestApiView.as_view()


class DeleteTestApiView(AddTestApiView):
    serializer_class = DeleteTestSerializer


delete_test = DeleteTestApiView.as_view()
