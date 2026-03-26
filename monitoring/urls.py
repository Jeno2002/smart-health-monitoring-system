from django.contrib import admin
from django.urls import path, include
from . import views
from .views import LogoutAPIView
from .views import LoginAPIView, RegisterAPIView, HealthMonitoringAPIView,LogoutAPIView,patient_form, health_result
from .views import health_monitoring, get_health_data


urlpatterns=[
    path('',views.home,name='home'),
    path('dashboard/',views.dashboard,name='dashboard'),
    path('login/',views.login,name='login'),
    path('logout/',views.logout,name='logout'),
    path('register/',views.register,name='register'),
    path('submit_health_data/',views.submit_health_data, name='submit_health_data'),
    path("patient_form/",views.patient_form, name="patient_form"),
    path('success/',views.success, name='success'),
    path('notification/', views.notification, name='notification'),
    path("api/get-latest-notifications/",views.get_latest_notifications, name="get_latest_notifications"),
    path('health_result/', views.health_result, name='health_result'),
    path('health_monitoring/',views.health_monitoring, name='health_monitoring'),
    path('api/health-data/<int:user_id>/', get_health_data, name='get_health_data'),


    path('check_up_count/', views.CheckUpCount.as_view(), name='check_up_count'),
    
    path('user_register/', RegisterAPIView.as_view()),
    path('user_login/', LoginAPIView.as_view()),
    path('user_health_monitoring/', HealthMonitoringAPIView.as_view()),
    path('/logout/', LogoutAPIView.as_view()),
    




    path('accounts/', include('django.contrib.auth.urls'))
]

