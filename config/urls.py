from django.contrib import admin
from django.urls import path, include
from restaurant_application.views import custom_logout

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('restaurant_application.urls')),
    path('accounts/logout/', custom_logout, name='logout'),
    path('accounts/', include('django.contrib.auth.urls')),
]
