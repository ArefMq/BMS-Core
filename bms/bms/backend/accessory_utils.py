from django.http import HttpResponse, JsonResponse
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from bms.backend.permissions import IsAdminOrReadOnly
from django.contrib.auth.models import User
from bms.backend.serializers import UserSerializer, UserProfileSerializer, ProfileUserSerializer, AccessoriesSerializer, GroupsSerializer, SceneSerializer, CommandSerializer
from bms.backend.models import Profile, Accessories, AccessoryGroups, Scenes, Command


def set_command_view_data(acc_id, status, is_analog=False, analog_value=0):
    acc = Accessories.objects.get(id=acc_id)
    if is_analog:
        acc.analogValue = analog_value
    else:
        acc.status = status
    acc.save()


def get_accessory_view_data(acc_id):
    accessory = Accessories.objects.get(id=acc_id)
    serializer = AccessoriesSerializer(accessory)
    
    if accessory.isAnalog:
        return accessory.analogValue
    else:    
        return accessory.status
