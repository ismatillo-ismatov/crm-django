from django.urls import path
from .views import *


app_name = 'app'

urlpatterns = [
    path('',LeadListView.as_view(),name='list'),
    path('create',LeadCreateView.as_view(),name="create"),
    path("<int:pk>/assign-agent",AssignAgentView.as_view(),name="assign-agent"),
    path('<int:pk>/',LeadDetailView.as_view(),name="detail"),
    path('<int:pk>/update/',LeadUpdateView.as_view(),name="update"),
    path("<int:pk>/delete/",LeadDeleteView.as_view(),name="delete"),
    path("categories/",CategoryListView.as_view(),name="category-list"),
    path("category-detail/<int:pk>/",CategoryDetailView.as_view(),name="category-detail"),
    path("category/<int:pk>/update",CategoryUpdateView.as_view(),name="lead_category-update"),
    path("create-category",CategoryCreateView.as_view(),name="category-create"),
    path("category-update/<int:pk>",UpdateCategoryView.as_view(),name="category_update")
]