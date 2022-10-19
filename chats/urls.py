from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . views import *
from . import views
router = DefaultRouter()


urlpatterns = [
    path('chats/', views.chats, name='chats'),
    path('friend/<str:pk>', views.detail, name="detail"),
    path('sent_msg/<str:pk>', views.sentMessages, name = "sent_msg"),
    path('rec_msg/<str:pk>', views.receivedMessages, name = "rec_msg"),
    path('notification', views.chatNotification, name = "notification"),
]