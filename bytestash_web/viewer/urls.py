from django.urls import path
from . import views

urlpatterns = [
    path('snippets/', views.snippet_list, name='snippet_list'),
    path('snippets/<int:snippet_id>/', views.snippet_detail, name='snippet_detail'),
]