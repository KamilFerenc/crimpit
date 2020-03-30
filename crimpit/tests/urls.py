from django.conf.urls import url

from crimpit.tests.api_views import campus_test_set_api_view, hangboard_test_set_api_view

urlpatterns = [
    url(r'^campus-tests/$', campus_test_set_api_view, name='campus_tests_list'),
    url(r'^hangboard-tests/$', hangboard_test_set_api_view, name='hangoard_tests_list')
]
