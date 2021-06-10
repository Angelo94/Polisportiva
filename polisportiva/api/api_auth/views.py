from django.contrib.auth import authenticate, login, logout
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from apps.users.models import User
from api.api_auth.serializers import UserSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets, generics
from rest_framework.views import APIView
from django.shortcuts import redirect


class UserRegistrationView(APIView):
    renderer_classes = [TemplateHTMLRenderer]

    def post(self, request, *args, **kwargs):
        try:
            if User.objects.filter(username=request.data['username'], email=request.data['email']).exists():
                return Response({"error": "User already exist"}, template_name='user/login.html')
            else:
                user = User.objects.create_user(username=request.data['username'],
                                                password=request.data['password'],
                                                email=request.data['email'],
                                                first_name=request.data['first_name'],
                                                last_name=request.data['last_name'])
                user.save()
                return Response({"info": "Now just log in"}, template_name='user/login.html')
        except:
            return Response({"error": "Error during the registration"}, template_name='user/login.html')


class UserViewSet(viewsets.ModelViewSet):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = (IsAuthenticated,)

    renderer_classes = [TemplateHTMLRenderer]
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def list(self, request, **kwargs):
        return Response({'users': self.queryset.all()}, template_name='user/users_list.html')


class HomeView(APIView):
    renderer_classes = [TemplateHTMLRenderer]

    def get(self, request, **kwargs):
        if request.user.is_authenticated:
           return Response({}, template_name='home/home.html')
        else:
           return Response({}, template_name='user/login.html')


class LoginView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    renderer_classes = [TemplateHTMLRenderer]

    def post(self, request, *args, **kwargs):

        if 'name' in request.data:
            user = User.objects.filter(username=request.data['name'])
        elif 'email' in request.data:
            user = User.objects.filter(email=request.data['email'])
        else:
            return Response({"error": "username or email not correct"}, template_name='user/login.html')

        if user:
            if user[0].check_password(request.data['password']):
                login(request, user[0])
                return redirect('home')
            else:
                return Response({"error": "User does not exist"}, template_name='user/login.html')
        else:
            return Response({"error": "User does not exist"}, template_name='user/login.html')


class LogoutView(APIView):
    renderer_classes = [TemplateHTMLRenderer]

    def post(self, request, *args, **kwargs):
        logout(request)
        return redirect('home')