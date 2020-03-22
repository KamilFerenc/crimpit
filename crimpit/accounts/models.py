import os

from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import ugettext_lazy as _

from crimpit.accounts.validators import validate_birth_date, validate_start_climbing

TRAINER = 'trainer'
ATHLETE = 'athlete'

USER_TYPE = (
    (TRAINER, _('Trainer')),
    (ATHLETE, _('Athlete'))
)


class CustomUser(AbstractUser):
    PROFILE_PHOTO_UPLOAD_FOLDER = os.path.join('admindata', 'images', 'users', '%Y', '%m', '%d')

    type = models.CharField(verbose_name=_('User type'), max_length=50, choices=USER_TYPE, default=ATHLETE)
    club = models.CharField(verbose_name=_('Sport Club'), max_length=50)
    birth_date = models.DateField(verbose_name=_('Birth date'), null=True, blank=True, validators=[validate_birth_date])
    start_climbing = models.PositiveIntegerField(verbose_name=_('Start climbing - year'), null=True, blank=True,
                                                 validators=[validate_start_climbing])
    profile_photo = models.ImageField(verbose_name=_('Profile photo'), blank=True,
                                      upload_to=PROFILE_PHOTO_UPLOAD_FOLDER)
    phone = models.CharField(verbose_name=_('Phone number'), max_length=16, blank=True)
    city = models.CharField(verbose_name=_('City'), max_length=20, blank=True)
    athletes = models.ManyToManyField('self', verbose_name=_('Athletes'), related_name='athletes')

    def __str__(self):
        return f"{self.pk} - {self.username}"


class AthleteManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        return super(AthleteManager, self).get_queryset().filter(type=ATHLETE, *args, **kwargs)


class Athlete(CustomUser):
    class Meta:
        proxy = True

    verbose_name = _('Athlete')
    verbose_name_plural = _('Athletes')

    objects = AthleteManager()


class TrainerManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        return super(TrainerManager, self).get_queryset().filter(type=TRAINER, *args, **kwargs)


class Trainer(CustomUser):
    class Meta:
        proxy = True
        verbose_name = _('Trainer')
        verbose_name_plural = _('Trainers')

    objects = TrainerManager()
