"""
URL configuration for app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from debug_toolbar.toolbar import debug_toolbar_urls

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("users.urls", namespace="users")),
    path("profile/",include("app_profile.urls",namespace='profile')),
    path("upload/",include("app_analysator.urls",namespace='analysator')),
    path("display/",include("app_display_data.urls",namespace="display_data")),
    path("download-char/",include("app_download_char.urls",namespace="download_char")),
] + debug_toolbar_urls()


if settings.DEBUG:  # Только для режима разработки
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)