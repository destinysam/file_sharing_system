from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import AuthenticationFailed
from rest_framework import serializers

class InvalidCredentials(AuthenticationFailed):
    default_detail = _("Invalid Credentials")




class InvalidFileFormat(serializers.ValidationError):
    pass   



class FileTooLarge(serializers.ValidationError):
    pass