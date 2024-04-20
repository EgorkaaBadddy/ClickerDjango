from django.shortcuts import render
from rest_framework import viewsets

# Create your views here.
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Core, Boost
from .serializers import CoreSerializer, BoostSerializer


@api_view(['GET'])
def call_click(request):
    core = Core.objects.get(user=request.user)
    is_levelup = core.click()
    if is_levelup:
        Boost.objects.create(core=core, price=core.coins, power=core.level * 2)
    core.save()

    return Response({'core': CoreSerializer(core).data, 'is_levelup': is_levelup})


@api_view(['POST'])
def update_coins(request):
    coins = request.data['current_coins']  # Значение current_coins будем присылать в теле запроса.
    core = Core.objects.get(user=request.user)

    is_levelup, boost_type = core.set_coins(
        coins)  # Метод set_coins скоро добавим в модель. Добавили boost_type для создания буста.

    # Дальнейшая логика осталась прежней, как в call_click
    if is_levelup:
        Boost.objects.create(core=core, price=core.coins, power=core.level * 2,
                             type=boost_type)  # Создание буста. Добавили атрибут type.
    core.save()

    return Response({
        'core': CoreSerializer(core).data,
        'is_levelup': is_levelup,
    })

@api_view(['GET'])
def get_core(request):
    core = Core.objects.get(user=request.user)
    return Response({'core': CoreSerializer(core).data})


class BoostViewSet(viewsets.ModelViewSet):
    queryset = Boost.objects.all()
    serializer_class = BoostSerializer

    def get_queryset(self):
        core = Core.objects.get(user=self.request.user)
        boosts = Boost.objects.filter(core=core)
        return boosts

    def partial_update(self, request, pk):
        coins = request.data['coins']  # Получаем количество монет из тела запроса.
        boost = self.queryset.get(pk=pk)

        is_levelup = boost.levelup(
            coins)  # Передадим количество монет в метод. Этот метод мы скоро немного подкорректируем.
        if not is_levelup:
            return Response({"error": "Не хватает денег"})
        old_boost_stats, new_boost_stats = is_levelup

        return Response({
            "old_boost_stats": self.serializer_class(old_boost_stats).data,
            "new_boost_stats": self.serializer_class(new_boost_stats).data,
        })
