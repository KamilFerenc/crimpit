from rest_framework import serializers

from crimpit.tests.models import TestSet, Exercise


class TestSetSerializer(serializers.ModelSerializer):
    creator = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = TestSet
        fields = ['id', 'title', 'level', 'creator', 'test_type', 'promoted', 'private', 'exercises']


class ExerciseSerializer(serializers.ModelSerializer):
    creator = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Exercise
        fields = ['id', 'title', 'creator', 'exercise_type', 'image', 'private', 'description']
