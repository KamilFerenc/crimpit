from django.conf.urls import url

from crimpit.accounts.api_views import athletes_list_api_view, trainers_list_api_view

urlpatterns = [
    url(r'athletes', athletes_list_api_view, name='athletes'),
    url(r'^trainers/$', trainers_list_api_view, name='trainers'),
]