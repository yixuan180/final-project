from django.urls import path
from . import views

urlpatterns = [
    path('generate-by-emotion/', views.generate_by_emotion, name='generate_by_emotion'),  
    path('', views.emotion_view, name='emotion'),  
    path('emotionResult/', views.emotion_result_view, name='emotionResult'),  
    path('emotionDetail/<int:id>/', views.emotion_detail, name='emotionDetail'),
]

