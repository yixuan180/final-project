from django.urls import path
from . import views

urlpatterns = [
    path('generate-by-emotion/', views.generate_by_emotion, name='generate_by_emotion'),
]
