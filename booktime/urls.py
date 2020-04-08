from django.contrib import admin as original_admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from main import admin


urlpatterns = [
    # path('original-admin/', original_admin.site.urls),
    path('admin/', admin.main_admin.urls),
    path('office-admin/', admin.central_office_admin.urls),
    path('dispatch-admin/', admin.dispatchers_admin.urls),

    path('api/v1/', include('api.urls')),

    path('', include('main.urls')),

    path('address/', include('users.urls')),
    path('accounts/', include('allauth.urls')),
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
