from .serializers import (RegistrationSerializer, VerifyOTPSerializer, 
                          ProfessionSerializer, MyTokenObtainPairSerializer,
                          UserPostSerializer, UserGetSerializer)
from rest_framework import generics, status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.parsers import MultiPartParser, FormParser
from core.emails import *
from core.models import User, Profession
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.throttling import ScopedRateThrottle
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
    throttle_scope = 'login'
    
    @swagger_auto_schema(tags=['Authentication'])
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
    
    
class RegistrationAPIView(generics.GenericAPIView):
    serializer_class = RegistrationSerializer
    
    @swagger_auto_schema(tags=['Authentication'])
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        data = {}
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            # send_otp(serializer.data['email'])
            data['response'] = 'Registration successful'
            refresh = RefreshToken.for_user(user=user)
            data['refresh'] = str(refresh)
            data['access'] = str(refresh.access_token)
        return Response(data, status.HTTP_201_CREATED)
    

class VerifyOTPAPIView(generics.GenericAPIView):
    @swagger_auto_schema(tags=['Authentication'])
    def post(self, request, *args, **kwargs):
        serializer = VerifyOTPSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.data['email']
            otp = serializer.data['otp']
            user_obj = User.objects.get(email=email)
            
            if user_obj.otp == otp:
                user_obj.is_staff = True
                user_obj.save()
                return Response("verified")
            return Response(serializer.data,status.HTTP_400_BAD_REQUEST)
        
        
class LogoutBlacklistTokenUpdateView(APIView):
    permission_classes = [permissions.AllowAny]
    authentication_classes = ()

    @swagger_auto_schema(tags=['Authentication'])
    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        
class UsersAPIView(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = User.objects.all()
    serializer_class = UserGetSerializer
    
    @swagger_auto_schema(tags=['Authentication'])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
    
    
class UserDetailAPIView(generics.RetrieveAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = User.objects.all()
    serializer_class = UserGetSerializer
    lookup_field = 'id'
    
    @swagger_auto_schema(tags=['Authentication'])
    def get(self, request, id, *args, **kwargs):
        return super().get(request, id, *args, **kwargs)
    

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny]
    parser_classes = (MultiPartParser, FormParser)
    # authentication_claes = [JWTAuthentication]
    lookup_field = 'id'
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return UserPostSerializer
        return UserGetSerializer 
    

class ProfessionViewSet(viewsets.ModelViewSet):
    queryset = Profession.objects.all()
    serializer_class = ProfessionSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = 'slug'