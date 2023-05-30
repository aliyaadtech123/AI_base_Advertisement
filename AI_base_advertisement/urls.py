
from django.urls import path,include
from ads_display import urls
from ads_display import views
from django.contrib import admin


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include(urls)),
    path('auth/',include('rest_framework.urls'))
]
