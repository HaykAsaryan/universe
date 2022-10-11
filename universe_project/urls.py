from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('', include('universe_app.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'universe_app.views.custom_page_not_found_view'
handler500 = 'universe_app.views.custom_error_view'
handler403 = 'universe_app.views.custom_permission_denied_view'
handler400 = 'universe_app.views.custom_bad_request_view'
