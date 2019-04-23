from rest_framework import serializers
from musics.models import Music

class MusicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Music
        # fields = '__all__'    # 返回全部属性
        fields = ('id', 'song', 'singer', 'last_modify_date', 'created')    # 返回自定义的属性