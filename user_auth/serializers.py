from rest_framework import serializers
from .models import CustomUser
from rest_framework.validators import UniqueValidator


# User register serializers

class CustomUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
    required = True,
    validators = [UniqueValidator(queryset=CustomUser.objects.all(),message="Email Already Exists")]
    )
    
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'password', 'full_name', 'email']
        extra_kwargs = {
            
            'password': {'write_only':True}
        }
        
        
    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance
    
    
    
class VerifyUserSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField()
    
    


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
    provider = serializers.CharField(required=False, allow_blank=True)
    
        
        
        
    