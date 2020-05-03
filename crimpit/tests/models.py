from django.db import models
from django.utils.translation import gettext_lazy as _

from crimpit.helpers.models import TimeStampModel

BEGINNER = 'beginner'
ADVANCED = 'advanced'
PRO = 'pro'

LEVEL_CHOICES = (
    (BEGINNER, _('Beginner')),
    (ADVANCED, _('Advanced')),
    (PRO, _('Pro'))
)

CAMPUS_BOARD = 'campus_board'
HANGBOARD = 'hangboard'

TYPE_CHOICES = (
    (CAMPUS_BOARD, _('Campus board')),
    (HANGBOARD, _('Hangboard'))
)


class TestSet(TimeStampModel):
    title = models.CharField(verbose_name=_('Title'), max_length=255)
    level = models.CharField(verbose_name=_('Level'), max_length=255, default=ADVANCED, choices=LEVEL_CHOICES)
    creator = models.ForeignKey('accounts.CustomUser', verbose_name=_('Creator'), on_delete=models.CASCADE)
    test_type = models.CharField(verbose_name=_('Test Type'), max_length=255,
                                 default=HANGBOARD, choices=TYPE_CHOICES)
    promoted = models.BooleanField(default=False, help_text=_('If True, test set will be promoted on the website'))
    private = models.BooleanField(default=False, help_text=_('If True, test set will be visible only for '
                                                             'creator or creator\'s athletes'))
    exercises = models.ManyToManyField('tests.Exercise', verbose_name=_('Exercises'),
                                       blank=True, related_name='test_sets')

    def __str__(self):
        return f'{self.pk} - {self.title}'


class CampusTestSetManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super(CampusTestSetManager, self).get_queryset().filter(test_type=CAMPUS_BOARD, *args, **kwargs)


class CampusTestSet(TestSet):
    class Meta:
        proxy = True
        verbose_name = _('Campus Test Set')
        verbose_name_plural = _('Campus Test Sets')

    objects = CampusTestSetManager()


class HangboardTestSetManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super(HangboardTestSetManager, self).get_queryset().filter(test_type=HANGBOARD, *args, **kwargs)


class HangboardTestSet(TestSet):
    class Meta:
        proxy = True
        verbose_name = _('Hangboard Test Set')
        verbose_name_plural = _('Hangboard Test Sets')

    objects = HangboardTestSetManager()


class Exercise(TimeStampModel):
    title = models.CharField(verbose_name=_('Title'), max_length=255)
    creator = models.ForeignKey('accounts.CustomUser', verbose_name=_('Creator'), on_delete=models.CASCADE)
    exercise_type = models.CharField(verbose_name=_('Exercise type'), max_length=255,
                                     default=HANGBOARD, choices=TYPE_CHOICES)
    image = models.ImageField(verbose_name=_('Image'), blank=True,
                              help_text=_('Add image how exercise should look like'))
    private = models.BooleanField(default=False, help_text=_('If True, test set will be visible only for '
                                                             'creator or creator\'s athletes'))
    description = models.TextField(verbose_name=_('Description'), blank=True,
                                   help_text=_('Write more details about exercise'))

    class Meta:
        verbose_name = _('Exercise')
        verbose_name_plural = _('Exercises')

    def __str__(self):
        return f'{self.pk} - {self.title}'


class CampusExerciseManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super(CampusExerciseManager, self).get_queryset().filter(exercise_type=CAMPUS_BOARD, *args, **kwargs)


class CampusExercise(Exercise):
    class Meta:
        proxy = True
        verbose_name = _('Campus Exercise')
        verbose_name_plural = _('Campus Exercises')

    objects = CampusExerciseManager()


class HangboardExerciseManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super(HangboardExerciseManager, self).get_queryset().filter(exercise_type=HANGBOARD, *args, **kwargs)


class HangboardExercise(Exercise):
    class Meta:
        proxy = True
        verbose_name = _('Hangboard Exercise')
        verbose_name_plural = _('Hangboard Exercises')

    objects = HangboardExerciseManager()
