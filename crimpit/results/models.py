from decimal import Decimal, ROUND_HALF_UP

from django.contrib.auth.models import AnonymousUser
from django.db import models
from django.utils.translation import ugettext_lazy as _

from crimpit.helpers.models import TimeStampModel


class Result(TimeStampModel):
    athlete = models.ForeignKey('accounts.CustomUser', verbose_name=_('Athlete'), related_name='results',
                                on_delete=models.SET_DEFAULT, default=AnonymousUser)
    campus_test = models.ForeignKey('tests.CampusTestSet', verbose_name=_('Campus rest'), blank=True, null=True,
                                    on_delete=models.PROTECT, related_name='campus_results')
    hangboard_test = models.ForeignKey('tests.HangboardTestSet', verbose_name=_('Hangboard test'), blank=True,
                                       null=True, on_delete=models.PROTECT, related_name='hangboard_results')
    athlete_weight = models.DecimalField(verbose_name=_('Weight'), max_digits=5, decimal_places=2)
    comment = models.TextField(verbose_name=_('Comment'), blank=True)


class CampusResult(TimeStampModel):
    result = models.ForeignKey('results.Result', verbose_name=_('Result'), related_name='campus_results',
                               on_delete=models.CASCADE)
    exercise = models.ForeignKey('tests.CampusExercise', verbose_name=_('Exercise'), on_delete=models.PROTECT)
    moves = models.PositiveIntegerField(verbose_name=_('Moves'))


class ExerciseResult(TimeStampModel):
    result = models.ForeignKey('results.Result', verbose_name=_('Result'), related_name='hangboard_results',
                               on_delete=models.CASCADE)
    exercise = models.ForeignKey('tests.HangboardExercise', verbose_name=_('Exercise'), on_delete=models.PROTECT)
    left_hand = models.DecimalField(verbose_name=_('Left hand result'), max_digits=5, decimal_places=2)
    percent_left = models.DecimalField(verbose_name=_('Left hand percent'), blank=True, null=True,
                                       max_digits=5, decimal_places=2)
    right_hand = models.DecimalField(verbose_name=_('Right hand result'), max_digits=5, decimal_places=2)
    percent_right = models.DecimalField(verbose_name=_('Left hand percent'), blank=True, null=True,
                                        max_digits=5, decimal_places=2)

    def save(self, *args, **kwargs):
        self.percent_left = Decimal(
            (((self.result.athlete_weight - self.left_hand) / self.result.athlete_weight) * 100).quantize(
                Decimal('.01'), rounding=ROUND_HALF_UP))
        self.percent_right = Decimal(
            (((self.result.athlete_weight - self.right_hand) / self.result.athlete_weight) * 100).quantize(
                Decimal('.01'), rounding=ROUND_HALF_UP))
        super(ExerciseResult, self).save(*args, **kwargs)
