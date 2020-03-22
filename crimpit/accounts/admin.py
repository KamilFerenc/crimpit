from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import ugettext_lazy as _

from crimpit.accounts.models import Athlete, Trainer


class AthleteAdmin(BaseUserAdmin):
    list_display = ('username', 'email',)
    readonly_fields = ('last_login', 'date_joined',)
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (_('Extra info'),
         {'fields': ('type', 'club', 'birth_date', 'start_climbing', 'phone', 'city', 'profile_photo')}),
        (_('Permissions'), {'classes': ('collapse',),
                            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )


admin.site.register(Athlete, AthleteAdmin)


class TrainerAdmin(AthleteAdmin):
    filter_horizontal = ('athletes',)


admin.site.register(Trainer, TrainerAdmin)
