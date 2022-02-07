from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from .views import MyRegistrationView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('rango/', include('rango.urls')),
    # alternative way of auth users using django-redux
    path('accounts/register/', MyRegistrationView.as_view(),
         name='registration_register'),
    path('accounts/', include('registration.backends.simple.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
