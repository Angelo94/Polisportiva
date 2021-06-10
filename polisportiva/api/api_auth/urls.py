from api.api_auth.views import UserViewSet, UserRegistrationView, HomeView, LoginView, LogoutView
from django.urls import path, include
from rest_framework.routers import DefaultRouter


class UserView(DefaultRouter.APIRootView):
    pass


class MyDefaultRouter(DefaultRouter):
    root_view_name = 'users'
    APIRootView = UserView


router = MyDefaultRouter()

router.register('user', UserViewSet, basename='users')


urlpatterns = [
    path('', include(router.urls)),
    path('userregistration/', UserRegistrationView.as_view(), name='userregistration'),
    path('home/', HomeView.as_view(), name='home'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

]