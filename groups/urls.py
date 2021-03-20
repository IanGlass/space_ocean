from django.urls import path

from . import views

app_name = 'groups'

urlpatterns = [
    path('posts/<slug:slug>/', views.SingleGroup.as_view(), name='single'),
    path('', views.ListGroups.as_view(), name='list'),
    path('new/', views.CreateGroup.as_view(), name='create')
]
