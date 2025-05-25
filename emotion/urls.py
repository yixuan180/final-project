from django.urls import path
from . import views

urlpatterns = [
    path('generate-by-emotion/', views.generate_by_emotion, name='generate_by_emotion'),
    path('emotionResult/', views.result_view, name='emotion_result'),
    path('', views.emotion_view, name='emotion'), 
]

