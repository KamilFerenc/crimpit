from decimal import Decimal, ROUND_HALF_UP

from django.contrib.auth.models import AnonymousUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from crimpit.helpers.models import TimeStampModel
from crimpit.results.validators import check_if_positive


class Result(TimeStampModel):
    user = models.ForeignKey('accounts.CustomUser', verbose_name=_('Athlete'), related_name='results',
                             on_delete=models.SET_DEFAULT, default=AnonymousUser)
    campus_test = models.ForeignKey('tests.CampusTestSet', verbose_name=_('Campus rest'), blank=True, null=True,
                                    on_delete=models.PROTECT, related_name='campus_results')
    hangboard_test = models.ForeignKey('tests.HangboardTestSet', verbose_name=_('Hangboard test'), blank=True,
                                       null=True, on_delete=models.PROTECT, related_name='hangboard_results')
    user_weight = models.DecimalField(verbose_name=_('Weight'), max_digits=5, decimal_places=2,
                                      validators=[check_if_positive])
    comment = models.TextField(verbose_name=_('Comment'), blank=True)

    def __str__(self):
        return f'Result {self.id}: {self.user.username} ({self.created.strftime("%Y-%m-%d")})'


class CampusResult(TimeStampModel):
    result = models.ForeignKey('results.Result', verbose_name=_('Result'), related_name='campus_results',
                               on_delete=models.CASCADE)
    exercise = models.ForeignKey('tests.CampusExercise', verbose_name=_('Exercise'), on_delete=models.PROTECT)
    moves = models.PositiveIntegerField(verbose_name=_('Moves'), blank=True, null=True)


class HangboardResult(TimeStampModel):
    result = models.ForeignKey('results.Result', verbose_name=_('Result'), related_name='hangboard_results',
                               on_delete=models.CASCADE)
    exercise = models.ForeignKey('tests.HangboardExercise', verbose_name=_('Exercise'), on_delete=models.PROTECT)
    left_hand = models.DecimalField(verbose_name=_('Left hand result'), blank=True, null=True,
                                    max_digits=5, decimal_places=2)
    percent_left = models.DecimalField(verbose_name=_('Left hand percent'), blank=True, null=True,
                                       max_digits=5, decimal_places=2)
    right_hand = models.DecimalField(verbose_name=_('Right hand result'), blank=True, null=True,
                                     max_digits=5, decimal_places=2)
    percent_right = models.DecimalField(verbose_name=_('Left hand percent'), blank=True, null=True,
                                        max_digits=5, decimal_places=2)

    def save(self, *args, **kwargs):
        if self.left_hand:
            self.percent_left = Decimal(
                (((self.result.user_weight - self.left_hand) / self.result.user_weight) * 100).quantize(
                    Decimal('.01'), rounding=ROUND_HALF_UP))
        if self.right_hand:
            self.percent_right = Decimal(
                (((self.result.user_weight - self.right_hand) / self.result.user_weight) * 100).quantize(
                    Decimal('.01'), rounding=ROUND_HALF_UP))
        super(HangboardResult, self).save(*args, **kwargs)
