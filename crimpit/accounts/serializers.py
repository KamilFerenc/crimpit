from rest_framework import serializers

from crimpit.accounts.models import CustomUser, COACH, ATHLETE


class CustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password_2 = serializers.CharField(write_only=True)
    type = serializers.ChoiceField(choices=(COACH, ATHLETE))
    email = serializers.EmailField(required=True)

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password', 'password_2', 'type', 'club', 'birth_date', 'start_climbing',
                  'profile_photo', 'phone', 'city')

    def validate(self, data):
        password = data['password']
        password_2 = data['password_2']
        if password != password_2:
            raise serializers.ValidationError({
                'password': 'Password don\'t match.',
                'password_2': 'Password don\'t match.'
            })
        return data

    def create(self, validated_data):
        validated_data.pop('password_2')
        user = CustomUser(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user
