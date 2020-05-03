from django.conf.urls import url

from crimpit.results.api_view import results_view, result_detail, start_test

urlpatterns = [
    url(r'^results/$', results_view, name='results_list'),
    url(r'^results/(?P<pk>\d+)$', result_detail, name='result_detail'),
    url(r'^start-test/$', start_test, name='start_test')
]
