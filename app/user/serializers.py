"""
Serializers for the user API view
"""
from django.contrib.auth import get_user_model

from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the user object"""

    class Meta:
        model = get_user_model()
        fields = ['email', 'password', 'name']
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}

    # Create method is built in. When a POST request is made, the create method
    # is automatically called during the object creation process

    # When POST request is made to an API view that uses the serializer,
    # the framework performs the deserialization, validation and object creation
    # steps behind the scene
    def create(self, validated_data):
        """Create and return a user with encrypted data"""
        return get_user_model().objects.create_user(**validated_data)
