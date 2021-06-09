from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from apps.users.models import User
from api.api_auth.serializers import UserSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets, generics
from rest_framework.views import APIView


class CustomObtainAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({'id': user.id, 'token': token.key})


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
        except Exception as e:
            return Response(e.__str__())


class UserViewSet(viewsets.ModelViewSet):
    renderer_classes = [TemplateHTMLRenderer]
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def list(self, request, **kwargs):
        #if request.user.is_authenticated:
        #    return Response({'users': self.queryset.all()}, template_name='user/users_list.html')
        #else:
        #    return Response({}, template_name='user/login.html')
        return Response({}, template_name='user/login.html')
