from django.conf.urls import url

from crimpit.accounts.api_views import (
    athletes_list_api_view, trainers_list_api_view, create_user_api_view, detail_update_user_api_view, add_test,
    delete_test
)

urlpatterns = [
    url('^register/$', create_user_api_view, name='register'),
    url(r'^athletes/$', athletes_list_api_view, name='athletes_list'),
    url(r'^trainers/$', trainers_list_api_view, name='trainers_list'),
    url(r'^user/(?P<pk>\d+)', detail_update_user_api_view, name='user_detail'),
    url(r'^add-tests/$', add_test, name='add_test'),
    url(r'^delete-tests/$', delete_test, name='delete_test')
]
