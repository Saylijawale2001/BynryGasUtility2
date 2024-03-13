from django.urls import path
from . import views
from .views import user_logout
 
urlpatterns = [
    path('login/', views.user_login, name='login'),
    path('', views.customer_signup, name='customer_signup'),
   # path('customer/signup/', views.customer_signup, name='customer_signup'),
    path('staff/signup/', views.staff_member_signup, name='staff_member_signup'),
    path('customer/service_request_form/', views.service_request_form, name='service_request_form'),
    path('customer/dashboard/', views.dashboard, name='dashboard'),
    path('customer/others/', views.Customer_home, name='others'),

    path('staff/dashboard/',views.staff_dashboard,name='staff-dashboard'),
    path('staff/edit_request/<int:id>',views.edit_request,name='edit_request'),

    # path('submit-service-request/', views.service_request_submit, name='submit_service_request'),
    path('account-information/', views.account_info, name='account_information'),
    path('logout/', user_logout, name='logout'),
]