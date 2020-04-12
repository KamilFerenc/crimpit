from django.conf.urls import url

from crimpit.tests.api_views import (
    campus_test_set, hangboard_test_set, campus_test_set_detail, hangboard_test_set_detail, hangboard_exercise,
    campus_exercise, campus_exercise_detail, hangboard_exercise_detail
)

urlpatterns = [
    url(r'^tests/campus/$', campus_test_set, name='campus_tests_list'),
    url(r'^tests/hangboard/$', hangboard_test_set, name='hangboard_tests_list'),
    url(r'^tests/campus/(?P<pk>\d+)/$', campus_test_set_detail, name='campus_test_detail'),
    url(r'^tests/hangboard/(?P<pk>\d+)/$', hangboard_test_set_detail, name='hangboard_test_detail'),
    url(r'^exercises/campus/$', campus_exercise, name='campus_exercises_list'),
    url(r'^exercises/hangboard/$', hangboard_exercise, name='hangboard_exercises_list'),
    url(r'^exercises/campus/(?P<pk>\d+)/$', campus_exercise_detail, name='campus_exercise_detail'),
    url(r'^exercises/hangboard/(?P<pk>\d+)/$', hangboard_exercise_detail, name='hangboard_exercise_detail'),
]
