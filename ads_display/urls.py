from django.urls import path,include
from ads_display import views
from .predictions import StartEnd
from rest_framework import routers
urlpatterns=[
    path('get_data/',views.data.as_view({"get":"list"}),name="get_data"),
    path('get_data/<int:pk>/',views.data.as_view({"get":"retrieve"}),name="get_data"), 
    path('del_data/<int:pk>',views.data.as_view({"delete":"destroy"}),name="del_data"),
    path('start/<str:status>/',StartEnd.as_view(),name="start")

]