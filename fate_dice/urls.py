from django.urls import path
from . import views

urlpatterns = [
    path('roll_dice/', views.roll_dice, name='roll_dice'),
    path('', views.fate_dice_view, name='fate_dice'), 
]
