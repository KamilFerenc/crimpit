from rest_framework import serializers


from crimpit.accounts.models import CustomUser, TRAINER, ATHLETE
from crimpit.tests.models import TestSet
from crimpit.tests.serializers import TestSetSerializer


class CustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password_2 = serializers.CharField(write_only=True)
    type = serializers.ChoiceField(choices=(TRAINER, ATHLETE))
    email = serializers.EmailField(required=True)
    athletes = serializers.PrimaryKeyRelatedField(read_only=True, required=False, many=True)
    tests = TestSetSerializer(read_only=True, required=False, many=True)

    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'password', 'password_2', 'type', 'club', 'birth_date', 'start_climbing',
                  'profile_photo', 'phone', 'city', 'athletes', 'tests')

    def validate_password_2(self, password_2):
        password = self.initial_data.get('password', None)
        if password != password_2:
            raise serializers.ValidationError('Password don\'t match.')
        return password_2

    def create(self, validated_data):
        validated_data.pop('password_2')
        user = CustomUser(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user


class AddTestSerializer(serializers.ModelSerializer):
    tests = serializers.PrimaryKeyRelatedField(queryset=TestSet.objects.all(), many=True)

    class Meta:
        model = CustomUser
        fields = ('tests',)

    def update(self, instance, validated_data):
        instance.tests.add(*self.validated_data.get('tests', None))
        instance.save()
        return instance


class DeleteTestSerializer(AddTestSerializer):
    def update(self, instance, validated_data):
        instance.tests.remove(*self.validated_data.get('tests', None))
        instance.save()
        return instance
