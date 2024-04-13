from django.urls import path

from backend.views import call_click
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.user_logout),
    path('registration/', views.Register.as_view(), name='registration'),
    path('users/<int:pk>/', views.UserDetail.as_view()),
    path('call_click/', call_click),
]
