from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin

api_urls = [
    url(r'', include('crimpit.accounts.urls')),
    url(r'', include('crimpit.tests.urls')),
]

urlpatterns = [
    url(r'admin/', admin.site.urls),
    url(r'api/', include(api_urls)),
    url(r'api-auth/', include('rest_framework.urls'))
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
