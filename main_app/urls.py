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
    path('project_data/', views.project_data, name='project_data'),
    path('taskpage/', views.task, name='taskpage'),
    path('task_detail/<int:id>', views.task_detail, name='taskdetail'),
    path('task_delete/<int:id>', views.delete_task, name='taskdelete'),
]
