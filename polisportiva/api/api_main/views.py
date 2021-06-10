from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView


class HomeView(APIView):
    renderer_classes = [TemplateHTMLRenderer]

    def get(self, request):
        if request.user.is_authenticated:
           return Response({}, template_name='home/home.html')
        else:
           return Response({}, template_name='user/login.html')
