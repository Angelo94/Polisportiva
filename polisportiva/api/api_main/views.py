from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from api.api_auth.serializers import UserSerializer


class HomeView(APIView):
    renderer_classes = [TemplateHTMLRenderer]

    def get(self, request):
        if request.user.is_authenticated:
           return Response({"user": request.user.username}, template_name='home/home.html')
        else:
           return Response({}, template_name='user/login.html')


class UserInfoView(APIView):
    renderer_classes = [TemplateHTMLRenderer]

    def get(self, request, *args, **kwargs):
        user_info = UserSerializer(request.user)
        return Response(user_info.data, template_name='user/users_list.html')