from rest_framework import serializers
from .models import Message
from rest_framework.generics import (CreateAPIView,GenericAPIView,)
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework import status
from file_management.models import File
from users.mixin import UserDetailSerializer
import time
# Create your views here.



class SendMessageSerializer(serializers.ModelSerializer):
    """"
    Input serializer to send message
    """

    class Meta:
        model = Message
        fields = ["message","file"]




class SendMessageAPI(CreateAPIView):
    """"
    API to send message
    """

    serializer_class = SendMessageSerializer
    permission_classes = [IsAuthenticated]


    def post(self,request,*args,**kwargs):
        user = get_object_or_404(User,id = request.user.id)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.validated_data["sender"] = user
        serializer.save()
        return Response(data={"message":"Message send successfully"},status=status.HTTP_201_CREATED)
    



class LongPoolingMessageSerializer(serializers.ModelSerializer):
    """"
    Output serializer to list file spacefied messages
    """

    sender = UserDetailSerializer()
    class Meta:
        model = Message
        fields = ["id","message","date_time","sender"]



    def to_representation(self, instance):
        representation =  super().to_representation(instance) 
        representation["date_time"] = instance.date_time.strftime("%B %d %Y %H:%M %p")   
        return representation



class LongPoolingFileMessageAPI(GenericAPIView):
    """"
    API to list file spacefied messages using long pooling
    """

    serializer_class = LongPoolingMessageSerializer
    permission_classes = [IsAuthenticated]

    lookup_url_kwarg = "file_id"

   

    def get(self,request,*args,**kwargs):
        
        file = get_object_or_404(File,id=self.kwargs["file_id"])
        last_message_id = request.GET.get("last_message_id",None)
        if last_message_id:
            qs = Message.objects.filter(file=file,id__gt=last_message_id).order_by("date_time")
        # sending messages in ascending order
        else:
            qs = Message.objects.filter(file=file).order_by("date_time")
        
        serializer = LongPoolingMessageSerializer(qs,many=True)
        return Response(data=serializer.data,status=status.HTTP_200_OK)



