from django.urls import path
from . import views

urlpatterns = [
    path('roll_dice/', views.roll_dice, name='roll_dice'),
    path('result.html', views.result_view, name='result'),
]
