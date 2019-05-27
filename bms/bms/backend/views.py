from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User

from rest_framework import viewsets, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token

from bms.backend.permissions import IsAdminOrReadOnly
from bms.backend.serializers import UserSerializer, UserProfileSerializer, ProfileUserSerializer, AccessoriesSerializer, GroupsSerializer, SceneSerializer, CommandSerializer
from bms.backend.models import Profile, Accessories, AccessoryGroups, Scenes, Command
from bms.backend.accessory_utils import set_command_view_data, get_accessory_view_data


class CustomObtainAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        response = super(CustomObtainAuthToken, self).post(
            request, *args, **kwargs)
        token = Token.objects.get(key=response.data['token'])
        serializer = UserProfileSerializer(
            token.user, context={'request': request})
        return Response({'success': True, 'message': '', 'data': {'token': token.key, 'user': serializer.data}})


@api_view(['GET', 'POST'])
#@permission_classes([permissions.IsAuthenticated])
def ProfileView(request):
    user = request.user
    if request.method == 'POST':
        user.profile.name = request.POST.get('name')
        user.profile.save()
        serializer = UserProfileSerializer(user, context={'request': request})
        return Response({'success': True, 'message': '', 'data': serializer.data})
    elif request.method == 'GET':
        serializer = UserProfileSerializer(user, context={'request': request})
        return Response({'success': True, 'message': '', 'data': serializer.data})
    return Response({'success': False, 'message': 'Something is wrong!!', 'data': ''})


@api_view(['POST'])
#@permission_classes([permissions.IsAuthenticated])
def ChangePassView(request):
    user = request.user
    if request.method == 'POST':
        user.set_password(request.POST.get('password'))
        user.save()
        serializer = UserProfileSerializer(user, context={'request': request})
        return Response({'success': True, 'message': '', 'data': serializer.data})
    return Response({'success': False, 'message': 'Something is wrong!!', 'data': ''})


@api_view(['POST'])
#@permission_classes([permissions.IsAuthenticated])
def UploadView(request):
    user = request.user
    if request.method == 'POST':
        user.profile.image = request.FILES['image']
        user.profile.save()
        serializer = UserProfileSerializer(user, context={'request': request})
        return Response({'success': True, 'message': 'Done!', 'data': serializer.data})
    return Response({'success': False, 'message': 'Something is wrong!!', 'data': ''})
# endregion
# region User


@api_view(['GET', 'POST'])
#@permission_classes([permissions.IsAdminUser])
def UserView(request):
    user = request.user
    if request.method == 'POST':
        u = User.objects.create_user(username=request.POST.get('username'),
                                     password=request.POST.get('password'),
                                     is_staff=request.POST.get('is_staff'))
        p = Profile(user=u, name=request.POST.get('name'),
                    house=House.objects.get(id=user.profile.house.id))
        p.save()
        serializer = UserProfileSerializer(u, context={'request': request})
        return Response({'success': True, 'message': '', 'data': {'users': serializer.data}})
    elif request.method == 'GET':
        profiles = Profile.objects.filter(house=user.profile.house)
        serializer = ProfileUserSerializer(profiles, many=True)
        return Response({'success': True, 'message': '', 'data': {'users': serializer.data}})
    return Response({'success': False, 'message': 'Something is wrong!!', 'data': ''})


@api_view(['POST'])
#@permission_classes([permissions.IsAdminUser])
def DeleteUserView(request):
    user = request.user
    if request.method == 'POST':
        u = User.objects.get(id=request.POST.get('userID'))
        u.delete()
        return Response({'success': True, 'message': 'Done!!', 'data': ''})
    return Response({'success': False, 'message': 'Something is wrong!!', 'data': ''})


@api_view(['POST'])
#@permission_classes([permissions.IsAdminUser])
def EditUserView(request):
    user = request.user
    if request.method == 'POST':
        u = User.objects.get(id=request.POST.get('userID'))
        u.is_staff = request.POST.get('is_staff')
        u.save()
        serializer = UserProfileSerializer(u, context={'request': request})
        return Response({'success': True, 'message': 'Done!!', 'data': serializer.data})
    return Response({'success': False, 'message': 'Something is wrong!!', 'data': ''})
# endregion
# region Accessories


@api_view(['GET'])
#@permission_classes([permissions.IsAuthenticated])
def AllAccessoriesView(request):
    user = request.user
    if request.method == 'GET':
        acc = Accessories.objects.filter(house_id=user.profile.house.id)
        serializer = AccessoriesSerializer(acc, many=True)
        return Response({'success': True, 'message': 'Done!!', 'data':  {'accessories': serializer.data}})
    return Response({'success': False, 'message': 'Something is wrong!!', 'data': ''})


@api_view(['GET'])
# @permission_classes([permissions.IsAuthenticated]) This should be remain commentted
def AccessoryView(request):
    # user = request.user
    if request.method == 'GET':
        result = get_accessory_view_data(acc_id=request.query_params.get('id'))
        return Response(result)
    return Response({'success': False, 'message': 'Something is wrong!!', 'data': ''})


@api_view(['POST'])
#@permission_classes([permissions.IsAuthenticated])
def EditAccessoriesView(request):
    user = request.user
    if request.method == 'POST':
        acc = Accessories.objects.get(id=request.POST.get('id'))
        acc.name = request.POST.get('name')
        acc.iconName = request.POST.get('iconName')
        acc.save()
        serializer = AccessoriesSerializer(acc)
        return Response({'success': True, 'message': 'Done!!', 'data':  {'accessories': serializer.data}})
    return Response({'success': False, 'message': 'Something is wrong!!', 'data': ''})
# endregion
# region Group


@api_view(['POST', 'GET'])
#@permission_classes([permissions.IsAuthenticated])
def GroupView(request):
    user = request.user
    if request.method == 'POST':
        group = AccessoryGroups(name=request.POST.get('name'),
                                iconName=request.POST.get('iconName'),
                                user=user)
        group.save()
        serializer = GroupsSerializer(group)
        return Response({'success': True, 'message': 'Done!!', 'data':  {'group': serializer.data}})
    elif request.method == 'GET':
        group = AccessoryGroups.objects.get(id=request.query_params.get('id'))
        serializer = GroupsSerializer(group)
        return Response({'success': True, 'message': 'Done!!', 'data':  {'group': serializer.data}})
    return Response({'success': False, 'message': 'Something is wrong!!', 'data': ''})


@api_view(['GET'])
#@permission_classes([permissions.IsAuthenticated])
def GroupListView(request):
    user = request.user
    if request.method == 'GET':
        acc = Accessories.objects.filter(house_id=user.profile.house.id)
        group = AccessoryGroups.objects.filter(user=user)
        s = AccessoriesSerializer(acc, many=True)
        serializer = GroupsSerializer(group, many=True)
        return Response({'success': True, 'message': 'Done!!', 'data':  {'groups': serializer.data, 'All': s.data}})
    return Response({'success': False, 'message': 'Something is wrong!!', 'data': ''})


@api_view(['POST'])
#@permission_classes([permissions.IsAuthenticated])
def DeleteGroupView(request):
    user = request.user
    if request.method == 'POST':
        group = AccessoryGroups.objects.get(id=request.POST.get('id'))
        group.delete()
        return Response({'success': True, 'message': 'Done!!', 'data': ''})
    return Response({'success': False, 'message': 'Something is wrong!!', 'data': ''})


@api_view(['POST'])
#@permission_classes([permissions.IsAuthenticated])
def EditGroupView(request):
    user = request.user
    if request.method == 'POST':
        group = AccessoryGroups.objects.get(id=request.POST.get('id'))
        group.name = request.POST.get('name')
        group.iconName = request.POST.get('iconName')
        group.save()
        serializer = GroupsSerializer(group)
        return Response({'success': True, 'message': 'Done!!', 'data': serializer.data})
    return Response({'success': False, 'message': 'Something is wrong!!', 'data': ''})
# endregion
# region Command


@api_view(['POST', 'GET'])
# @permission_classes([permissions.IsAuthenticated])
def CommandView(request):
    user = request.user
    if request.method == 'POST':
        request_data = request.POST
    elif request.method == 'GET':
        request_data = request.query_params

    params = {
        'acc_id': request_data.get('id'),
        'status': request_data.get('command', 0),
        'is_analog': request_data.get('is_analog', False),
        'analog_value': request_data.get('analog_value', 0),
    }
    set_command_view_data(**params)
    return Response({'success': True, 'message': 'Done!!', 'data': ''})

# endregion
# region scene


@api_view(['GET'])
#@permission_classes([permissions.IsAuthenticated])
def SceneListView(request):
    user = request.user
    if request.method == 'GET':
        scenes = Scenes.objects.filter(user=user)
        serializer = SceneSerializer(scenes, many=True)
        # A = SceneAccessories.objects.all()
        # serializer = SceneAccessoriesSerializer(A, many=True)
        return Response({'success': True, 'message': 'Done!!', 'data':  {'scenes': serializer.data}})
    return Response({'success': False, 'message': 'Something is wrong!!', 'data': ''})


@api_view(['POST'])
#@permission_classes([permissions.IsAuthenticated])
def TrigerView(request):
    user = request.user
    if request.method == 'POST':
        commands = Command.objects.filter(scene=request.POST.get('id'))
        # a = CommandSerializer(command, many=True)
        for command in commands:
            if request.POST.get('command') == 'True':
                command.accessory.status = command.command
            else:
                command.accessory.status = False
            command.accessory.save()
        # A = SceneAccessories.objects.all()
        # serializer = SceneAccessoriesSerializer(A, many=True)
        return Response({'success': True, 'message': 'Done!!', 'data': ''})
    return Response({'success': False, 'message': 'Something is wrong!!', 'data': ''})
# endregion

@api_view(['GET'])
#@permission_classes([permissions.IsAuthenticated])
def HomePageView(request):
    pass