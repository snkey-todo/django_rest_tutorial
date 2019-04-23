from django.db import models

# Create your models here.
class Music(models.Model):
    """
    song,歌曲
    singer,歌手
    last_modify_date,更新时间
    created，创建时间


    default=“”，设置默认值
    auto_now=True，自动以当前时间为更新时间
    auto_now_add=True，自动添加当前时间为创建时间
    """
    song = models.TextField(default="song") 
    singer = models.TextField(default="AKB48")
    last_modify_date = models.DateTimeField(auto_now=True)  
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "music"