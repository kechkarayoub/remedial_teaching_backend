from django.urls import path

from . import views

urlpatterns = [
    path('check_if_email_or_username_exists', views.check_if_email_or_username_exists, name='check_if_email_or_username_exists'),
    path('login_with_token/', views.LoginTokenView.as_view(), name="login_with_token"),
    path('register/', views.RegisterView.as_view(), name="register"),
    path('resend_activation_email/', views.ResendActivationEmailView.as_view(), name="resend_activation_email"),
    path('users_test_api', views.users_test_api, name='users_test_api'),
]
