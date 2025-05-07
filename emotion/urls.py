from django.urls import path
from . import views

urlpatterns = [
    path('generate-by-emotion/', views.generate_itinerary, name='generate_by_emotion'),
]
