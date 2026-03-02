from .models import Task
from rest_framework import serializers
from django.contrib.auth.models import User



class TaskSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Task
        fields = ['id', 'user', 'title', 'description', 'is_completed', 'due_date', 'create_at', 'updated_at']
        read_only_fields = ['id', 'create_at', 'updated_at']


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
