from django.urls import path,include
from .views import SignUpAPI,SigninAPI,RefreshAccessTokenAPI

urlpatterns = [
    path("signup/",SignUpAPI.as_view(),name="signup"),
    path("signin/",SigninAPI.as_view(),name="login"),
    path("refresh_token/",RefreshAccessTokenAPI.as_view(),name="refresh-token"),
]    