from rest_framework import serializers


from crimpit.accounts.models import CustomUser, TRAINER, ATHLETE


class CustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password_2 = serializers.CharField(write_only=True)
    type = serializers.ChoiceField(choices=(TRAINER, ATHLETE))
    email = serializers.EmailField(required=True)

    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'password', 'password_2', 'type', 'club', 'birth_date', 'start_climbing',
                  'profile_photo', 'phone', 'city')

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
