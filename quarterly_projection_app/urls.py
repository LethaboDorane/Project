# quarterly_projection_app/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('projection/', views.quarterly_projection_view, name='quarterly_projection'),  # Ensure this name matches
    path('download_graph/', views.download_graph, name='download_graph'),
]
