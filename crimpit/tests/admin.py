from django.contrib import admin

from crimpit.tests.models import CampusTestSet, HangboardTestSet, CampusExercise, HangboardExercise


class TestSetBaseAdmin(admin.ModelAdmin):
    readonly_fields = ('created', 'modified')
    list_display = ('title', 'creator', 'private', 'level')
    raw_id_fields = ('creator',)
    filter_horizontal = ('exercises',)
    search_fields = ('level', 'creator')


admin.site.register(CampusTestSet, TestSetBaseAdmin)
admin.site.register(HangboardTestSet, TestSetBaseAdmin)


class ExerciseBaseAdmin(admin.ModelAdmin):
    readonly_fields = ('created', 'modified')
    list_display = ('title', 'creator', 'private')
    raw_id_fields = ('creator',)
    search_fields = ('level', 'creator')


admin.site.register(CampusExercise, ExerciseBaseAdmin)
admin.site.register(HangboardExercise, ExerciseBaseAdmin)
