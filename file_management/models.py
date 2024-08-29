from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
# Create your models here.


class File(models.Model):
    uploader = models.ForeignKey(User,verbose_name=_("file uploader"),on_delete=models.CASCADE)
    file = models.FileField(_("file"),upload_to="uploads/")
    reciepient = models.ForeignKey(User,verbose_name=_("reciepient"),related_name="recieved_files",on_delete=models.CASCADE)
    upload_date = models.DateTimeField(auto_now_add=True)



    def __str__(self):
        return f"{self.file.name} was uploaded by {self.uploader.username}"