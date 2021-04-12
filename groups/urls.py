from django.urls import path

from . import views

app_name = 'groups'

urlpatterns = [
    path('details/<slug:slug>', views.SingleGroup.as_view(), name='single'),
    path('', views.ListGroups.as_view(), name='list'),
    path('new', views.CreateGroup.as_view(), name='create'),
    path('join/<slug:slug>', views.JoinGroup.as_view(), name='join'),
    path('leave/<slug:slug>', views.LeaveGroup.as_view(), name='leave')
]
