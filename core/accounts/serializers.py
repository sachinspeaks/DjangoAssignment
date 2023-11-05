from rest_framework import serializers
from django.contrib.auth.models import User



class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=["email","password","first_name","last_name"]

    def validate_password(self, value):
        if not value:
            raise serializers.ValidationError("Email and password are required.")
        if len(value)<8:
            raise serializers.ValidationError("This password is too short. It must contain at least 8 characters")
        return value

    def validate_email(self, value):
        if not value:
            raise serializers.ValidationError("Email and password are required.")
        return value
    
    def validate(self, data):
        for _,val in data:
            if len(val)>100:
                raise serializers.ValidationError("Only 100 characters are allowed for a field")
        return data


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True,allow_blank=False)
    password = serializers.CharField(required=True,allow_blank=False,min_length=8)

class EditSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=["first_name","last_name","username"]

        def validate(self,data):
            if User.objects.filter(username=data["username"]).exists():
                raise serializers.ValidationError("User already exist with the username {}".format(data["username"]))
            return data
        
        
