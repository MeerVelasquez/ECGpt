from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('chatbot/', views.chatbot, name='chatbot'),
    path('dashboard/', views.dashboard, name='dashboard'),

]
