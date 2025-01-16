from core.models import User
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from core.models import User, Profession



class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        return token
    
    
class RegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    class Meta:
        model = User
        fields =  ['username', 'email', 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True}
        }
    def save(self):
        password = self.validated_data['password']
        password2 = self.validated_data['password2']

        if password != password2:
            raise serializers.ValidationError(
                {'error': 'passwords did not match'})

        user = User(
            username=self.validated_data['username'],
            email=self.validated_data['email'], 
            is_active=True
        )
        user.set_password(self.validated_data['password'])
        user.save()
        return user
    
    
class VerifyOTPSerializer(serializers.Serializer):

    email = serializers.EmailField()
    otp = serializers.CharField()
   
class ProfessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profession
        fields = ['id', 'title', 'slug', 'order', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['slug', 'created_at', 'updated_at'] 
    
class UserGetSerializer(serializers.ModelSerializer):
    # profession = ProfessionSerializer(read_only=True)
    
    class Meta:
        model = User
        fields = [
                    'id', 
                    'username', 
                    'email', 
                    'fullname', 
                    'type', 
                    'biography', 
                    'first_name', 
                    'last_name', 
                    'middle_name',
                    'address'
                    # 'profession', 
                    'type', 
                    'phone_number', 
                    'img', 
                    'thumbnail', 
                    'slug', 
                    'is_active', 
                    'order'
                ]
        read_only_fields = ['slug', 'is_active']

class UserPostSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = [
                    'id', 
                    'username', 
                    'email', 
                    'fullname', 
                    'type', 
                    'biography', 
                    'first_name', 
                    'last_name', 
                    'middle_name',
                    'address'
                    'profession', 
                    'type', 
                    'phone_number', 
                    'img', 
                    'thumbnail', 
                    'slug', 
                    'is_active', 
                    'order'
                ]
        read_only_fields = ['slug', 'is_active', 'fullname']
    
    
    

        
        