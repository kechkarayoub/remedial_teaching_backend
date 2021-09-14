from django.urls import path

from . import views

urlpatterns = [
    path('users_test_api', views.users_test_api, name='users_test_api'),
    path('login_with_token/', views.LoginTokenView.as_view(), name="login_with_token"),
]
