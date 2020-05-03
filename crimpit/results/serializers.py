from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from crimpit.results.models import Result, HangboardResult, CampusResult
from crimpit.tests.serializers import ExerciseSerializer


class BaseSingleResultSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        """Return all data for the exercise"""
        result = super().to_representation(instance)
        result['exercise'] = ExerciseSerializer(instance.exercise).data
        return result


class HangboardResultSerializer(BaseSingleResultSerializer):
    percent_left = serializers.DecimalField(read_only=True, max_digits=5, decimal_places=2)
    percent_right = serializers.DecimalField(read_only=True, max_digits=5, decimal_places=2)

    class Meta:
        model = HangboardResult
        fields = ('id', 'result', 'exercise', 'left_hand', 'right_hand', 'percent_left', 'percent_right', 'created',)


class CampusResultSerializer(BaseSingleResultSerializer):
    class Meta:
        model = CampusResult
        fields = ('id', 'result', 'exercise', 'moves', 'created',)


class ResultSerializer(serializers.ModelSerializer):
    hangboard_results = HangboardResultSerializer(many=True, required=False)
    campus_results = CampusResultSerializer(many=True, required=False)

    class Meta:
        model = Result
        fields = ('id', 'user', 'campus_test', 'hangboard_test', 'user_weight', 'comment', 'created',
                  'hangboard_results', 'campus_results',)

    def validate_user(self, user):
        if user not in self.context['request'].user.athletes.all():
            raise serializers.ValidationError(_('You can\'t create result for user who is not your athlete.'))
        return user

    def create_exercises_result(self, result, exercises, serializer_cls):
        for exercise in exercises:
            data = {
                'result': result.pk,
                'exercise': exercise.pk
            }
            serializer = serializer_cls(data=data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()

    def create(self, validated_data):
        if not self.validated_data.get('user', None):
            self.validated_data['user'] = self.context['request'].user
        result = Result.objects.create(**self.validated_data)
        campus_exercises = result.campus_test.exercises.all() if result.campus_test else []
        self.create_exercises_result(result, campus_exercises, CampusResultSerializer)
        hangboard_exercises = result.hangboard_test.exercises.all() if result.hangboard_test else []
        self.create_exercises_result(result, hangboard_exercises, HangboardResultSerializer)
        result.refresh_from_db()
        return result

    def update_hangboard_results(self, hangboard_results):
        for result in hangboard_results:
            try:
                hangboard_result = HangboardResult.objects.get(pk=result.get('pk'))
            except HangboardResult.DoesNotExist:
                continue
            if result.get('left_hand'):
                hangboard_result.left_hand = result.get('left_hand')
            if result.get('right_hand'):
                hangboard_result.right_hand = result.get('right_hand')
            hangboard_result.save(update_fields=['left_hand', 'right_hand'])

    def update_campus_results(self, campus_results):
        for result in campus_results:
            try:
                campus_result = CampusResult.objects.get(pk=result.get('pk'))
            except CampusResult.DoesNotExist:
                continue
            if result.get('moves'):
                campus_result.moves = result.get('moves')
            campus_result.save(update_fields=['moves'])

    def update(self, instance, validated_data):
        self.update_hangboard_results(self.initial_data.get('hangboard_results', []))
        self.update_campus_results(self.initial_data.get('campus_results', []))
        instance.user_weight = validated_data.get('user_weight', instance.user_weight)
        instance.comment = validated_data.get('comment', instance.comment)
        instance.save(update_fields=['user_weight', 'comment'])
        return instance
