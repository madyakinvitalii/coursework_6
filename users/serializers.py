from django.contrib.auth.password_validation import validate_password
from djoser.serializers import UserCreateSerializer
from rest_framework import serializers
from django.contrib.auth import get_user_model


User = get_user_model()


class UserRegistrationSerializer(UserCreateSerializer):
    password = serializers.CharField(write_only=True)

    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ['email', 'first_name', 'last_name', 'password', 'phone', 'image']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'phone', 'id', 'email', 'image']


class ChangePasswordSerializer(serializers.ModelSerializer):
    current_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, validators=[validate_password])

    def validate(self, data):
        user = self.context['request'].user
        current_password = data.get('current_password')
        new_password = data.get('new_password')

        if not user.check_password(current_password):
            raise serializers.ValidationError({'current_password': 'Wrong password'})

        if current_password == new_password:
            raise serializers.ValidationError('Similar password')

        return data

    class Meta:
        model = User
        fields = ['new_password', 'current_password']
