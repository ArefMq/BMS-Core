from django.contrib.auth.models import User
from bms.backend.models import Accessories, AccessoryGroups, Profile, House, Command, Scenes
from rest_framework import serializers


class HouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = House
        fields = ('id', 'name', 'GUID')


class ProfileSerializer(serializers.ModelSerializer):
    house = HouseSerializer(read_only=True)

    class Meta:
        model = Profile
        fields = ('image', 'name', 'house')

    def get_image(self, obj):
        return self.context['request'].build_absolute_uri(obj.image)


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'is_staff')
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        user = User(
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class UserProfileSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()

    class Meta:
        model = User
        fields = ('id', 'username', 'is_staff', 'profile')


class ProfileUserSerializer(serializers.ModelSerializer):
    house = HouseSerializer(read_only=True)
    user = UserSerializer()

    class Meta:
        model = Profile
        fields = ('image', 'name', 'house', 'user')

    def get_image(self, obj):
        return self.context['request'].build_absolute_uri(obj.image)


class AccessoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Accessories
        fields = ('id', 'name', 'status', 'iconName', 'AccType')


class GroupsSerializer(serializers.ModelSerializer):
    accessories = AccessoriesSerializer(read_only=True, many=True)

    class Meta:
        model = AccessoryGroups
        fields = ('id', 'name', 'iconName', 'accessories')


class CommandSerializer(serializers.ModelSerializer):
    accessory = AccessoriesSerializer()

    class Meta:
        model = Command
        fields = ('id', 'command', 'accessory')


class SceneSerializer(serializers.ModelSerializer):
    commands = CommandSerializer(many=True)

    class Meta:
        model = Scenes
        fields = ('id', 'name', 'iconName', 'commands')
        # , 'sceneaccessories')
