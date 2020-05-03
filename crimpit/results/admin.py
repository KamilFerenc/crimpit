from django.contrib import admin

from crimpit.results.models import Result, CampusResult, HangboardResult


class CampusAdminInline(admin.TabularInline):
    model = CampusResult
    extra = 0


class HangboardResultInline(admin.TabularInline):
    model = HangboardResult
    readonly_fields = ['percent_left', 'percent_right']
    extra = 0


class ResultAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'user', 'created']
    inlines = [CampusAdminInline, HangboardResultInline]
    readonly_fields = ['created', 'modified']


admin.site.register(Result, ResultAdmin)
