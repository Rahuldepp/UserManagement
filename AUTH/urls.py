from django.urls import path,include
from django.contrib.auth import views as auth_views
from  .views import *



urlpatterns = [
 
 

   path('login/',login_user,name='login_user'),
   path('forgot_email_password/',forgot_email_password,name='forgot_email_password'),
   path('register/',register,name='register'),
   path('mail_send/',verify_email_otp,name='mail_send'),
   path('success/',success,name='success'),
  #  path('verify/<auth_token>',verify,name='verify'),
   path('update_email_password',update_email_password,name='update_email_password'),
   
   path('logout/',logout_user,name='logout_user'),
 ]

