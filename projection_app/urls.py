# sales_projection_project/urls.py
from django.urls import path
from projection_app import views
from . import views


urlpatterns = [
    path('', views.sales_projection_view, name='sales_projection'),
]

urlpatterns = [
    path('', views.sales_projection_view, name='sales_projection'),
    path('download-graph/', views.download_graph, name='download_graph'),
    # Other URL patterns
    path('download-graph/<str:graph_data>/', views.download_graph, name='download_graph'),  # Add this line
]
