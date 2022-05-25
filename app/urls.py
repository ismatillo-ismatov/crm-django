from django.urls import path
from .views import (
    LeadListView,LeadDetailView,LeadCreateView,LeadUpdateView,LeadDeleteView
)


app_name = 'app'

urlpatterns = [
    path('',LeadListView.as_view(),name='list'),
    path('create',LeadCreateView.as_view(),name="create"),
    path('<int:pk>/',LeadDetailView.as_view(),name="detail"),
    path('<int:pk>/update/',LeadUpdateView.as_view(),name="update"),
    path("<int:pk>/delete/",LeadDeleteView.as_view(),name="delete"),
]