from rest_framework import serializers

from crimpit.tests.models import TestSet, Exercise


class TestSetSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestSet
        fields = ['id', 'title', 'level', 'creator', 'test_type', 'promoted', 'private', 'exercises']


class ExerciseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exercise
        fields = ['id', 'title', 'creator', 'exercise_type', 'image', 'private', 'description']
