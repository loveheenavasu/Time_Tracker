from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from .views import MyTokenObtainPairView, CustomViewSet, index, profilesetting
from rest_framework_simplejwt.views import TokenRefreshView
from . import views
router = DefaultRouter()
router.register(r'register', CustomViewSet, basename='register'),

urlpatterns = [
    path('', views.login_session, name="login_session"),
    path('router/', include(router.urls)),
    path('login/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('loginpage', views.login_session, name="login_session"),
    path('logout/', views.logout_view, name="logout"),
    path('index/', views.index, name="index"),
    path('user_profile/<int:id>', views.user_profile, name='user_profile'),
    path('all_users/', views.all_users, name='all_users'),
    path('project_detail/<int:id>', views.projects_details, name='project_detail'),
    path('delete/<int:id>', views.delete_user, name='delete'),
    path('update_project/<int:id>', views.update_project, name='project_update'),
    path('delete_project/<int:id>', views.delete_project, name='project_delete'),
    path('export/excel', views.export_users_xls, name='export_excel'),
    path('export_excel_projects/', views.export_projects_xls, name='export_excel_project'),
    path('forgetpassword/', views.forgetpassword, name='forgetpassword'),
    path('activate/user/<int:user_id>', views.user_activate, name='activate_user'),
    path('deactivate/user/<int:user_id>', views.user_deactivate, name='deactivate_user'),
    path('profilesetting/<int:id>', views.profilesetting, name='profilesetting'),   
] 


if settings.DEBUG:
     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


