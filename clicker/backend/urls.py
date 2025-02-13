from django.urls import path, include
from . import views

boosts = views.BoostViewSet.as_view({
    'get': 'list',
    'post': 'create',
})


lonely_boost = views.BoostViewSet.as_view({
    'put' : 'partial_update',
})


urlpatterns = [
    path('', include('auth_clicker.urls')),
    path('call_click/', views.call_click, name='call_click'),
    path('boosts/', boosts, name='boosts'),
    path('boost/<int:pk>/', lonely_boost, name='boost'),
    path('update_coins/', views.update_coins),
    path('core/', views.get_core)
]

