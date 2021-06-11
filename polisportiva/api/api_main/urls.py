from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.api_main.views import HomeView, UserInfoView


class UserView(DefaultRouter.APIRootView):
    pass


class MyDefaultRouter(DefaultRouter):
    root_view_name = 'users'
    APIRootView = UserView


urlpatterns = [
    path('home/', HomeView.as_view(), name='home'),
    path('userinfo/', UserInfoView.as_view(), name='userinfo'),

]