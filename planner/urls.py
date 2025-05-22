from django.urls import path
from . import views  



urlpatterns = [
    path('', views.planner_view, name='planner'),
    path('generate_itinerary/', views.generate_itinerary, name='generate_itinerary'),  # 呼叫 generate_itinerary 函數處理該路由
    
]
