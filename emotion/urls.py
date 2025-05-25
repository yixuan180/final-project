from django.urls import path
from . import views

urlpatterns = [
    path('generate-by-emotion/', views.generate_by_emotion, name='generate_by_emotion'),
    path('result/', views.result_view, name='result'),
    path('', views.emotion_view, name='emotion'),  # 根路由，不要加 emotion/
]

