from rest_framework import serializers
from .models import Message
from rest_framework.generics import CreateAPIView,GenericAPIView
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework import status
from file_management.models import File
from users.mixin import UserDetailSerializer
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
    



class ListFileMessageSerializer(serializers.ModelSerializer):
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


class ListFileMessageAPI(GenericAPIView):
    """"
    API to list file spacefied messages
    """

    serializer_class = ListFileMessageSerializer
    permission_classes = [IsAuthenticated]

    lookup_url_kwarg = "file_id"

   

    def get(self,request,*args,**kwargs):
        file = get_object_or_404(File,id=self.kwargs["file_id"])
        # sending messages in ascending order
        qs = Message.objects.filter(file=file)
        serializer = ListFileMessageSerializer(qs,many=True)
        return Response(data=serializer.data,status=status.HTTP_200_OK)



