from django.urls import path, include
from . import views


boosts = views.BoostViewSet.as_view({'get': 'list','post' : 'create'})


urlpatterns = [
    path('', include('auth_clicker.urls')),
    path('call_click/', views.call_click, name='call_click'),
    path('boosts/', boosts, name='boosts'),
]

