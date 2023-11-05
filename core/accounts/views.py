from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from .serializers import SignUpSerializer,LoginSerializer,EditSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.contrib.auth import authenticate
from firebase_admin import auth
import uuid
# Create your views here.

def getUserName(first_name,last_name):
    username=first_name+"_"+last_name+str(uuid.uuid4())[:4]
    while User.objects.filter(username=username).exists():
        username=first_name+last_name+str(uuid.uuid4())[:4]
    return username
    

@api_view(['POST'])
def register(request):
    data=request.data
    user=SignUpSerializer(data=data)
    if user.is_valid():
        # print(user.data)
        if not User.objects.filter(username=data.get("username")).exists():
            user=User.objects.create(
                email=data.get("email"),
                first_name=data.get("first_name"),
                last_name=data.get("last_name"),
                username=getUserName(data.get("first_name"),data.get("last_name")),
                password=make_password(data.get("password")),
            )
            return Response({"username":user.username,"email":user.email},status=status.HTTP_200_OK)
        else:
            return Response({"error":"A user with that username already exists"},status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(user.errors,status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def login(request):
    data = request.data
    serializer = LoginSerializer(data=data)
    if serializer.is_valid():
        print(serializer)
        username=serializer.data.get("username")
        password = serializer.data.get("password")
        user = authenticate(request=request,username=username, password=password)

        if user is None:
            return Response(
                {"error": "Username or password is invalid"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        print("reached here")
        custom_token = auth.create_custom_token(user.username)
        return Response({"token": custom_token}, status=status.HTTP_200_OK)

    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def view(request):
    # data=request.data
    # user=User.objects.get(username=username)
    print('--<')
    # full_name=user.first_name+" "+user.last_name
    # return Response({"username":user.username,"email":user.email,"full_name":full_name},status=status.HTTP_200_OK)
    # user = request.user
    # print("-->", user)
    return Response({"success": "true"})
            

api_view(["POST"])
def edit(request):
    data=request.data
    obj=User.objects.get(id=data['username'])
    serializer=EditSerializer(obj,data=data,partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data,status=status.HTTP_200_OK)
    else:
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)