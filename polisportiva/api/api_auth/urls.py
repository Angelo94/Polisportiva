from api.api_auth.views import UserRegistrationView, LoginView, LogoutView, UserInfoView
from django.urls import path, include
from rest_framework.routers import DefaultRouter


class UserView(DefaultRouter.APIRootView):
    pass


class MyDefaultRouter(DefaultRouter):
    root_view_name = 'users'
    APIRootView = UserView

urlpatterns = [
    path('userregistration/', UserRegistrationView.as_view(), name='userregistration'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('userinfo/', UserInfoView.as_view(), name='userinfo'),
]