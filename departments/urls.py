from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . views import DeparmentsViewSet
from . import views
router = DefaultRouter()
router.register(r'departments', DeparmentsViewSet, basename='department'),

urlpatterns = [
    path('', include(router.urls)),
    path('department_details/<str:name>', views.department_info, name='department_details'),
    path('departments_/', views.departments, name='admin_departments'),
    path('screenshots/', views.screenshorts, name='screenshots'),
    path('update_department_project/', views.update_project_department, name='update_department_project'),
    path('delete_department/<int:id>', views.delete_department, name='delete_department')

]


