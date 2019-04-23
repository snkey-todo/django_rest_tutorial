from django.db import models

# Create your models here.
class Share(models.Model):
    name = models.TextField(default="SNKEY")
    last_modify_date = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "share"
