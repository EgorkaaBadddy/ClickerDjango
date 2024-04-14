from django.apps import apps
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from rest_framework import generics
from rest_framework.views import APIView
from backend.models import Core
from .forms import UserForm
from .serializers import UserSerializer, UserSerializerDetail


# Create your views here.

class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializerDetail


# def index(request):
#     user = User.objects.filter(id=request.user.id)
#     if len(user) != 0:
#         core = Core.objects.get(user=request.user)
#         return render(request, 'index.html',{'core' : core})
#     else:
#         return redirect('login')


def index(request):
    coreModel = apps.get_model('backend', 'Core')
    boostsModel = apps.get_model('backend', 'Boost')
    core = coreModel.objects.get(user=request.user)
    boosts = boostsModel.objects.filter(core=core)

    return render(request, 'index.html',{
        'core' : core,
        'boosts' : boosts,
    })

def user_logout(request):
    logout(request)
    return redirect('login')


class Register(APIView):
    def get(self, request):
        form = UserForm()
        return render(request, 'registration.html', {'form': form})

    def post(self, request):
        form = UserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            existing_user = User.objects.filter(username=username)
            if len(existing_user) == 0:
                password = form.cleaned_data['password']
                user = User.objects.create_user(username, '', password)
                user.save()
                user = authenticate(request, username=username, password=password)
                login(request, user)
                core = Core(user=user)
                core.save()
                return redirect('index')
            else:
                return render(request, 'registration.html', {'invalid': True, 'form': form})

class Login(APIView):
    def get(self, request):
        return render(request, 'login.html', {'invalid': False})
    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            return render(request, 'login.html', {'invalid': True})




# def user_registration(request):
#     if request.method == 'POST':
#         form = UserForm(request.POST)
#         if form.is_valid():
#             username = form.cleaned_data['username']
#             existing_user = User.objects.filter(username=username)
#             if len(existing_user) == 0:
#                 password = form.cleaned_data['password']
#                 user = User.objects.create_user(username, '', password)
#                 user.save()
#                 user = authenticate(request, username=username, password=password)
#                 login(request, user)
#                 return redirect('index')
#             else:
#                 return render(request, 'registration.html', {'invalid': True, 'form': form})
#     else:
#         form = UserForm()
#         return render(request, 'registration.html', {'invalid': False, 'form': form})

# def user_login(request):
#     if request.method == 'POST':
#         username = request.POST['username']
#         password = request.POST['password']
#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             login(request, user)
#             return redirect('index')
#         else:
#             return render(request, 'login.html', {'invalid': True})
#
#     else:
#         return render(request, 'login.html', {'invalid': False})