from django.urls import path
from . import views

urlpatterns = [
    path('', views.fate_dice_view, name='fate_dice'), 
    path('roll_dice/', views.roll_dice, name='roll_dice'),
    path('fate_diceResult/', views.fate_diceResult_view, name='fate_diceResult'),
    path('fate_diceDetail/', views.fate_diceDetail_view, name='fate_diceDetail'),
]
