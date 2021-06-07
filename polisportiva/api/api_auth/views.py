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
    def post(self, request, *args, **kwargs):
        try:
            if User.objects.filter(username=request.data['username'], email=request.data['email']).exists():
                return Response('Username already exists', 400)
            else:
                user = User.objects.create_user(username=request.data['username'], password=request.data['password'],
                                                email=request.data['email'])
                user.save()
                return Response("User created", 200)
        except Exception as e:
            return Response(e.__str__())


class UserViewSet(viewsets.ModelViewSet):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'user/users_list.html'
    permission_classes = (IsAuthenticated,)
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        response = super(UserViewSet, self).list(request, *args, **kwargs)

        #serializer_data = UserSerializer(self.queryset, many=True)
        return Response({'users': response.data})


class UsersList(generics.ListAPIView):
    queryset = User.objects.all()
    renderer_classes = [TemplateHTMLRenderer]

    def list(self, request):
        return Response({'users': self.queryset.all()}, template_name='users_list.html')
