from rest_framework import serializers
from django.contrib.auth.models import User,auth
from rest_framework.generics import (CreateAPIView,GenericAPIView,)
from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework.response import Response
from .exceptions import InvalidCredentials
from django.utils.translation import gettext_lazy as _
from .service import (get_login_token,get_token_from_refresh_token,)
# Create your views here.

class SignUpSerializer(serializers.ModelSerializer):
    """
    Input serializer for user signup
    """
    class Meta:
        model = User
        fields = ["first_name","last_name","username","email","password"]
        


class SignUpAPI(CreateAPIView):
    """
    API to hanlding user signup
    """
    serializer_class = SignUpSerializer
    permission_class = [AllowAny]


    def post(self,request,*args,**kwargs):
        serializer = self.get_serializer(data = request.data)
        if serializer.is_valid(raise_exception=True):
            user = User(
                first_name=serializer.validated_data['first_name'],
                last_name=serializer.validated_data['last_name'],
                username=serializer.validated_data['username'],
                email=serializer.validated_data['email']
            )
            user.set_password(serializer.validated_data['password'])  # Hash the password
            user.save()
        return Response(data={"message":"You have completed signup, congrats"},status=status.HTTP_200_OK)
    






class SigninSerializer(serializers.Serializer):
    """
    Input serializer for user signin
    """

    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)



class SigninAPI(GenericAPIView):
    """"
    API to hanle user signin
    """

    serializer_class = SigninSerializer
    permission_classes = [AllowAny]

    def post(self,request,*args,**kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = dict(serializer.validated_data)    
        user = auth.authenticate(**data)
        print(user)
        if not user:
            raise InvalidCredentials(_("Invalid username or password"))
            
        token = get_login_token(request,user)    
        return Response(data=token,status=status.HTTP_200_OK)
    





class RefreshAccessTokenSerializer(serializers.Serializer):
   """"
   Input serializer to get access token from refresh token
   """

   refresh_token = serializers.CharField()


class RefreshAccessTokenAPI(GenericAPIView):
    """"
    API to get access token from refresh token
    """


    serializer_class =RefreshAccessTokenSerializer
    



    def post(self,request,*args,**kwargs):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = dict(serializer.validated_data)
        refresh_token = data.get("refresh_token")
        refresh_token = get_token_from_refresh_token(refresh_token)
        return Response(data=refresh_token,status=status.HTTP_200_OK)