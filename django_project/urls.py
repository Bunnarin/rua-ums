from django.contrib import admin
from django.urls import path, include
from apps.core.views import home_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('session/', include('apps.core.urls')),
    path('accounts/', include('allauth.urls')),
    path('activities/', include('apps.activities.urls')),
    path('users/', include('apps.users.urls')),
    path('academic/', include('apps.academic.urls')),
    path('', home_view, name='home'),
]   
