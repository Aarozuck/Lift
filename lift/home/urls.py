from django.urls import path
from . import views

urlpatterns = [
    path('', views.intro, name='intro'),
    path('driver-home/', views.driver_home, name='driver-home'),
    path('rider-home/', views.rider_home, name='rider-home'),
    path('driver/login/', views.driver_login, name='driver_login'),
    path('driver/registration/', views.driver_registration, name='driver_registration'),
    path('rider/request-ride/<int:driver_id>/', views.request_ride, name='request-ride'),
    path('rider/login/', views.rider_login, name='rider_login'),
    path('rider/registration/', views.rider_registration, name='rider_registration'),
    path('driver-profile/', views.driver_profile, name='driver-profile'),
    path('rider-profile/', views.rider_profile, name='rider-profile'),
    path('driver/logout/', views.driver_logout, name='driver_logout'),
    path('rider/logout/', views.rider_logout, name='rider_logout'),
    path('update-driver-info/', views.update_driver_info, name='update-driver-info'),
      path('driver/accept-ride-request/<int:ride_request_id>/', views.accept_ride_request, name='accept-ride-request'),
    path('driver/decline-ride-request/<int:ride_request_id>/', views.decline_ride_request, name='decline-ride-request'),
    #path('service/', views.service_view, name='service'),
]
