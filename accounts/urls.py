from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MyTokenObtainPairView, CustomViewSet, index
from rest_framework_simplejwt.views import TokenRefreshView
from . import views
router = DefaultRouter()
router.register(r'register', CustomViewSet, basename='register'),

urlpatterns = [
    path('', include(router.urls)),
    path('login/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('loginpage', views.login_session, name="login_session"),
    path('index/', views.index, name="index"),
    path('registerpage/', views.home_view, name='register_session'),
    path('admin_register/', views.admin_register, name='admin_register'),
    path('user_profile/<int:id>', views.user_profile, name='user_profile'),
    path('all_users/', views.all_users, name='all_users'),
    path('delete/<int:id>', views.delete_user, name='delete'),
    path('index2/', views.index2, name='index2'),
]


