from django.contrib.auth import login
from django.shortcuts import redirect, get_object_or_404
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.decorators import permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from api.api_auth.serializers import UserSerializer
from apps.users.models import User


class HomeView(APIView):
    renderer_classes = [TemplateHTMLRenderer]

    def get(self, request):
        if request.user.is_authenticated:
           return Response({"user": request.user.username}, template_name='home/home.html')
        else:
           return Response({}, template_name='user/login.html')


@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
class UserInfoView(APIView):
    renderer_classes = [TemplateHTMLRenderer]

    def get(self, request, *args, **kwargs):
        user_info = UserSerializer(request.user)
        return Response(user_info.data, template_name='user/users_list.html')

    def post(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save(is_active=True)
        return redirect('userinfo')
