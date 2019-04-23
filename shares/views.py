# Create your views here.
from rest_framework import viewsets, status
from rest_framework.decorators import permission_classes
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from shares.models import Share
from shares.serializers import ShareSerializer

# Create your views here.
class ShareViewSet(viewsets.ModelViewSet):
    queryset = Share.objects.all()
    serializer_class = ShareSerializer
    # 指定这个view的 Content-Type 是 application/json
    parser_classes = (JSONParser,)

    def get_permissions(self):
        if self.action in ('create',):
            self.permission_classes = [IsAuthenticated]
        return [permission() for permission in self.permission_classes]

    # [GET] api/share/, 不需要授权
    def list(self, request, **kwargs):
        users = Share.objects.all()
        serializer = ShareSerializer(users, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    # [POST] api/share/，需要授权，添加@permission_classes注解，会调用get_permissions()方法
    @permission_classes((IsAuthenticated,))
    def create(self, request, **kwargs):
        name = request.data.get('name')
        users = Share.objects.create(name=name)
        serializer = ShareSerializer(users)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
