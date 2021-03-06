"""start URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path, re_path, include
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('study/', include('study.urls', namespace='study')),
    path('studypost/', include('studypost.urls', namespace='studypost')),
    path('assignment/', include('assignment.urls', namespace='assignment')),
    path('attendance/', include('attendance.urls', namespace='attendance')),
    path('table/', include('table.urls', namespace='table')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)



from django.conf.urls import url
if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
    url(r'^__debug__/', include(debug_toolbar.urls)),
    ]