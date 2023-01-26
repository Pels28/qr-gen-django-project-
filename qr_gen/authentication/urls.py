from django.contrib import admin
from django.urls import path, include
from .views import signup, home, UsernameValidationView, EmailValidationView, FirstNameValidationView, LastNameValidationView, ActivateView, loginView, RequestPasswordResetEmail, CompletePasswordReset
from django.views.decorators.csrf import csrf_exempt
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('signup', signup.as_view(), name="signup"),
    path('validate-username', csrf_exempt(UsernameValidationView.as_view()), name="validate-username"),
    path('validate-email', csrf_exempt(EmailValidationView.as_view()), name="validate-email"),
    path('validate-firstname', csrf_exempt(FirstNameValidationView.as_view()), name="validate-firstname"),
    path('validate-lastname', csrf_exempt(LastNameValidationView.as_view()), name="validate-lastname"),
    path('login', loginView.as_view(), name="login"),
#     path('logout', views.logout, name="logout"),
    path('activate/<uidb64>/<token>', ActivateView.as_view(), name="activate"),
    path('request-reset-link', RequestPasswordResetEmail.as_view(), name='request-password'),
    path('set-new-password/<uidb64>/<token>', CompletePasswordReset.as_view(), name='reset-user-password')
 ]