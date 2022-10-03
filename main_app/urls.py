from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . views import *
from . import views
router = DefaultRouter()
router.register(r'task', TaskViewSet, basename='taskcreations'),
router.register(r'projects', ProjectsViewSet, basename='project'),
router.register(r'remarks', RemarksViewSet, basename='remark'),

urlpatterns = [
    path('', include(router.urls)),
    path('project/', views.project, name='project'),
    path('taskpage/', views.task, name='task'),
    path('demo/', views.demo, name='demo'),
    path('logindemo', views.logindemo, name='logindemo')
]
