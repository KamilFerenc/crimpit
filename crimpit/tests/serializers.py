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


class ExerciseFiled(serializers.PrimaryKeyRelatedField):
    def get_queryset(self):
        queryset = Exercise.objects.filter(exercise_type=self.context.get('test_type', None))
        return queryset


class AddExerciseSerializer(serializers.ModelSerializer):
    exercises = ExerciseFiled(many=True)

    class Meta:
        model = TestSet
        fields = ['exercises']

    def update(self, instance, validated_data):
        instance.exercises.add(*self.validated_data['exercises'])
        instance.save()
        return instance


class DeleteExerciseSerializer(serializers.ModelSerializer):
    exercises = serializers.PrimaryKeyRelatedField(queryset=Exercise.objects.all(), many=True)

    class Meta:
        model = TestSet
        fields = ['exercises']

    def update(self, instance, validated_data):
        instance.exercises.remove(*self.validated_data['exercises'])
        instance.save()
        return instance
