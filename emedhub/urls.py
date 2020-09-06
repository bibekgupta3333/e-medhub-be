
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf.urls.static import static
from django.conf import settings

from django.views.generic import TemplateView
import django_schema


urlpatterns = [
    path('api-auth/', include('rest_framework.urls')),

    path('api/accounts/', include('accounts.urls', namespace='accounts')),
    path('api/store/', include('store.urls', namespace='store')),
    path('api/orders/', include('orders.urls', namespace='orders')),
    path('admin/', admin.site.urls),
    path('schema/', include('django_schema.urls')),


]
# urlpatterns += [re_path(r'^.*',
#                         TemplateView.as_view(template_name='index.html'))]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
