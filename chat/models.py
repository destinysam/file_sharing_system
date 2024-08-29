from django.db import models
from django.utils.translation import gettext_lazy  as _
from django.contrib.auth.models import User
from file_management.models import File
# Create your models here.

class Message(models.Model):
    message = models.TextField(verbose_name=_("message"))
    sender = models.ForeignKey(User,verbose_name=_("sender"),on_delete=models.CASCADE)
    file = models.ForeignKey(File,verbose_name=_("file"),on_delete=models.CASCADE)
    date_time = models.DateTimeField(verbose_name=_("date time"),auto_now_add=True)



    def __str__(self):
        return self.message