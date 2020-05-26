from django.urls import path

from . import views

urlpatterns = [
    path('', views.game_list, name='game_list'),
    path('<int:pk>/', views.game, name='game'),
    path('<int:pk>/log/', views.log, name='log')
]