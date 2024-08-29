from rest_framework import serializers
from .models import File
from rest_framework.generics import CreateAPIView,GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from users.exceptions import FileTooLarge
from django.utils.translation import gettext_lazy as _
from users.mixin import UserDetailSerializer
from django.conf import settings
from django.core.validators import FileExtensionValidator


# Create your views here.


MAX_FILE_SIZE = 5 * 1024 * 1024

class FileUploadSerializer(serializers.ModelSerializer):
    """"
    Input serializer to upload file
    """
    file = serializers.FileField(validators=[FileExtensionValidator(allowed_extensions=["jpeg","png","jpg","pdf","docx","doc"])])
    class Meta:
        model = File
        fields = ["file","reciepient"]

    def validate_file(self,value):
           
        
        if value.size > MAX_FILE_SIZE:
            raise FileTooLarge(_("File is too large please check select other file"))
            
        return value

            
        


class FileUploadAPI(CreateAPIView):
    """"
    API to upload a file
    """

    serializer_class = FileUploadSerializer
    permission_classes = [IsAuthenticated]


    def post(self,request,*args,**kwargs):
        user = get_object_or_404(User,id=self.request.user.id)
        serializer = FileUploadSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.validated_data["uploader"] = user
        serializer.save()
        return Response("File uploaded and transferred successfully",status=status.HTTP_201_CREATED)


class BaseFileSerializer(serializers.ModelSerializer):
    """
    Base output serializer
    """

    def to_representation(self, instance):
        representation =  super().to_representation(instance) 
        representation["upload_date"] = instance.upload_date.strftime("%B %d %Y %H:%M %p")   
        return representation    

    def get_file(self,obj):
      
        request = self.context.get("request")
        file_url = obj.file.url
        if request is not None:
            return request.build_absolute_uri(file_url)
        else:
            return f"{settings.MEDIA_URL}{obj.file.name}"  
        

class ListFileUploadSerializer(BaseFileSerializer):
    """"
    Output serializer to list uploaded files
    """

    reciepient = UserDetailSerializer()
    class Meta:
        model = File
        fields = ["reciepient","file","upload_date"]

    def to_representation(self, instance):
        representation =  super().to_representation(instance) 
        representation["upload_date"] = instance.upload_date.strftime("%B %d %Y %H:%M %p")   
        return representation    

    def get_file(self,obj):
      
        request = self.context.get("request")
        file_url = obj.file.url
        if request is not None:
            return request.build_absolute_uri(file_url)
        else:
            return f"{settings.MEDIA_URL}{obj.file.name}"
    


class ListFileUploadAPI(GenericAPIView):
    """"
    API to list user uploaded files
    """
    serializer_class = ListFileUploadSerializer
    permission_classes = [IsAuthenticated]   


    def get(self,request,*args,**kwargs):
        user = get_object_or_404(User,id=request.user.id) 
        file_uploads = File.objects.filter(uploader=user.id)  
        serializer = ListFileUploadSerializer(file_uploads,many=True,context={"request":request})  
        return Response(data=serializer.data,status=status.HTTP_200_OK)
    

  



class ListRecievedFileSerializer(BaseFileSerializer):
    """"
    Output Serializer to list recieved files
    """

    uploader = UserDetailSerializer()
    class Meta:
        model = File
        fields = ["uploader","file","upload_date"]

   
class ListRecievedFileAPI(GenericAPIView):
    """"
    API to list user recieved files
    """

    serializer_class = ListRecievedFileSerializer
    permission_classes = [IsAuthenticated]  



    def get(self,request,*args,**kwargs):
        user = get_object_or_404(User,id=request.user.id)  
        recieved_files = File.objects.filter(reciepient=user.id)
        serializer = ListRecievedFileSerializer(recieved_files,many=True,context={"request":request}) 
        return Response(data=serializer.data,status=status.HTTP_200_OK)

