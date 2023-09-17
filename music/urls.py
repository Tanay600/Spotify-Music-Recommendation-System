from django.urls import path
from . import views

urlpatterns = [
    path('', views.recommend_track, name='recommend_track'),  # URL for the recommendation page
]
