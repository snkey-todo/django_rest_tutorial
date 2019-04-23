# django_rest_tutorial

django rest framework tutorial

基于[django_basic](https://github.com/zhusheng/django_basic)进行迭代

## 配置rest framework

- 安装rest framework
`pip install djangorestframework`

说明：通过`pip list |grep djangorestframework`查一下安装结果和软件版本，在requirements.txt文件中添加软件信息作为备忘。。

- 配置。在settings.py中添加该框架，代码如下：

```python
INSTALLED_APPS = [
    ...
    'rest_framework',
    ...
]
```

- 序列化。序列化是rest framework很核心的一个部分，主要功能是将Python结构序列化为其它标准格式，如最常用的JSON。我们在musics app下新建`serializers.py`文件，代码如下：

```python
from rest_framework import serializers
from musics.models import Music

class MusicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Music
        # fields = '__all__'    # 返回全部属性
        fields = ('id', 'song', 'singer', 'last_modify_date', 'created')    # 返回自定义的属性
```

- 修改我们的view。添加如下代码，我们就拥有了rest框架提供的CRUD功能。

```python
from musics.models import Music
from musics.serializers import MusicSerializer
from rest_framework import viewsets

# Create your views here.
class MusicViewSet(viewsets.ModelViewSet):
    queryset = Music.objects.all()
    serializer_class = MusicSerializer
```

- 修改我们的主urls.py。我们使用rest框架为我们提供的路由方式来快速创建路由，这样我们就可以在浏览器进行访问，代码如下：

```python
from musics import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('music', views.MusicViewSet) # http://127.0.0.1:8000/api/music/

urlpatterns = [
    ...
    path('api/', include(router.urls)), # http://127.0.0.1:8000/api/
    ...
]
```

运行效果如下：
![image](https://raw.githubusercontent.com/zhusheng/blog/master/django/04.png)

## API测试

我们使用Postman测试API `http://127.0.0.1:8000/api/music/`的CRUD。

示例运行效果如下：
![image](https://raw.githubusercontent.com/zhusheng/blog/master/django/05.png)

## 授权 (Authentications)

在 REST API 中，授权很重要，如果没有授权，任何人都可以随意的不受限制的操作我的API，只是非常危险的，所以授权非常重要。rest framework为我们提供了授权功能，我们只需要简单配置一下即可实现。

- 在views.py中增加如下代码:

```python
from rest_framework.permissions import IsAuthenticated
# Create your views here.
class MusicViewSet(viewsets.ModelViewSet):
    ...
    permission_classes = (IsAuthenticated,)
```

完整的views.py如下所示：

```python
from musics.models import Music
from musics.serializers import MusicSerializer
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
# Create your views here.
class MusicViewSet(viewsets.ModelViewSet):
    queryset = Music.objects.all()
    serializer_class = MusicSerializer
    permission_classes = (IsAuthenticated,)
```

- 在主urls.py中增加如下代码:

```python
urlpatterns = [
    ...
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    ...
]
```

- 重新测试API,我们发现需要进行授权操作了。如下图所示：
![image](https://raw.githubusercontent.com/zhusheng/blog/master/django/06.png)
我们需要通过`python3 manage.py createsuperuser`获得一个用户，然后登录才能访问我们的API。用户名：`zhusheng`、密码:`zhusheng`，我们重新使用PostMan进行测试，如下所示：
![image](https://raw.githubusercontent.com/zhusheng/blog/master/django/07.png)

## 局部授权（Authentications）

我们新建一个app，名称为share,用于在其中设置我们的授权api,参考本项目的`share/views.py`

## Parser

在 REST framework 中有一个 Parser classes ，这个 Parser classes 主要是能控制接收的 Content-Type ，通常如果没有特别去设定的话，默认采用的是application / x-www-form-urlencode ， 但是这个可能不是我们想要的，我们可以进行手动设置。

### 全局设置

在`settings.py`中增加如下代码，代表全局只允许 

```python
REST_FRAMEWORK = {
    'DEFAULT_PARSER_CLASSES': (
        'rest_framework.parsers.JSONParser',
    )
}
```

### 局部设置

我们也可以只针对某些 view 或 viewsets 进行设置，我们直接在views.py 加上 parser_classes 即可

```python
class MusicViewSet(viewsets.ModelViewSet):
    queryset = Music.objects.all()
    serializer_class = MusicSerializer
    permission_classes = (IsAuthenticated,)
    parser_classes = (JSONParser,)
```

当然，parser_classes 不只有 JSONParser，还有 FormParser ， MultiPartParser 等等

[更多可參考官方文档](http://www.django-rest-framework.org/api-guide/parsers/#parsersr)

## Extra link and actions

我们在使用 rest framework时，难免需要制定一些额外的route，这时我们可以使用 `@detail_route` 或 `@list_route`。

### @detail_route

用于获取详情。

```python
@detail_route(methods=['get'],)
def song_detail(self, request, pk=None):
    music = get_object_or_404(Music, pk=pk)
    result = {
        'singer': music.singer,
        'song': music.song,
    }

    return Response(result, status=status.HTTP_200_OK)
```

以上这个例子的 `URL pattern: /api/music/{pk}/song_detail/` ，运行效果如下：

如果没有额外的指定，通常方法名就是url_path名。当然我们也可以指定url_path名，只需在注解中，增加`url_path='xx'`参数即可，例如`url_path='detail_self'`，示例如下：

```python
@detail_route(methods=['get'], url_path='detail_self')
...
```

### @list_route

用于显示列表

```python
@list_route(methods=['get'])
def all_singer(self, request):
    music = Music.objects.values_list('singer', flat=True).distinct()

    return Response(music, status=status.HTTP_200_OK)
```

以上这个例子的 `URL pattern: /api/music/all_singer/`, 我们也可以同理定义url_path名。