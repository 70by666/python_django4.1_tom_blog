from rest_framework import serializers

from apps.blog.models import Posts
from apps.users.models import User


class PostsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Posts
        fields = '__all__'
        
        
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ('password',)
