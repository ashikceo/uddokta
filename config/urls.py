from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import render
from store.admin_site import custom_admin_site


def handler404(request, exception):
    return render(request, '404.html', status=404)


def handler500(request):
    return render(request, '500.html', status=500)


urlpatterns = [
    path('admin/', custom_admin_site.urls),
    path('accounts/', include('allauth.urls')),
    path('', include('store.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
