from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve  # <-- Added to serve media files in production
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

# Media file routing configuration
if settings.DEBUG:
    # 1. Local Development Mode: Serves media files quickly using standard debug helpers
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
else:
    # 2. Production Cloud Mode: Explicitly bypasses Django's DEBUG restriction to route media files 
    # to your dynamic slider/banner storage directory (e.g., inside Defang or Docker volumes).
    urlpatterns += [
        path(f"{settings.MEDIA_URL.lstrip('/')}<path:path>", serve, {'document_root': settings.MEDIA_ROOT}),
    ]
