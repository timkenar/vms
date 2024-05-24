from django.shortcuts import render

# Create your views here.

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth import authenticate
from .serializers import Userserializer
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.authtoken.models import Token

from .models import CustomUser



# class CustomViewSet(viewsets.ModelViewSet):
#     queryset = Visitor.objects.all()
#     serializer_class = VisitorSerializer

@api_view(['POST'])
def register_user(request):
    if request.method == 'POST':
        serializer = Userserializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
def user_login (request):
    if request.method == 'POST':
        username = request.data.get('username')
        password = request.data.get('password')

        user = None
        if '@' in username:
            try:
                user = CustomUser.objects.get(email=username)
            except: ObjectDoesNotExist
            pass
        
        if not user:
            user = authenticate(username=username, password=password)
        
        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response ({'token':token.key}, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def user_logout(request):
    request.user.auth_token.delete()
    try:
        request.user.auth_token.delete()
        return Response({'message':'Successfully logged out.'}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    