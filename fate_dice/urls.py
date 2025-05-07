from django.urls import path
from . import views

urlpatterns = [
    path('roll-dice/', views.roll_dice, name='roll_dice'),
]
