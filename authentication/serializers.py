from django.contrib.auth.models import Group
from rest_framework import serializers


from . import models


class UserSerializer(serializers.HyperlinkedModelSerializer):
  class Meta:
    model   = models.User
    fields  = ['url', 'username', 'email', 'groups','password']
    extra_kwargs = {
      'password': {'write_only': True, 'required': True},
      'groups': {'required': False},
    }


class GroupSerializer(serializers.HyperlinkedModelSerializer):
  class Meta:
    model   = Group
    fields  = ['url', 'name']