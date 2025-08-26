from rest_framework import serializers
from ..models import Profile
from auth_app.models import CustomUser


class ProfileSerializer(serializers.ModelSerializer):
    """
    Main serializer for Profile objects.
    Used for retrieving and updating profile information.
    """
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.CharField(source='user.email', read_only=True)
    type = serializers.CharField(source='user.type', read_only=True)

    class Meta:
        model = Profile
        fields = ['user', 'username', 'first_name', 'last_name', 'file', 'location', 
                 'tel', 'description', 'working_hours', 'type', 'email', 'created_at']
        read_only_fields = ['user', 'created_at']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        for field in ['first_name', 'last_name', 'location', 'tel', 'description', 'working_hours']:
            if data[field] is None:
                data[field] = ''
        if data.get('user') is None:
            data['user'] = 0
        return data


class ProfileListSerializer(serializers.ModelSerializer):
    """
    Serializer for listing business profiles.
    Excludes email and created_at fields.
    """
    username = serializers.CharField(source='user.username', read_only=True)
    type = serializers.CharField(source='user.type', read_only=True)

    class Meta:
        model = Profile
        fields = ['user', 'username', 'first_name', 'last_name', 'file', 'location', 
                 'tel', 'description', 'working_hours', 'type']
        read_only_fields = ['user', 'username', 'type']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        for field in ['first_name', 'last_name', 'location', 'tel', 'description', 'working_hours']:
            if data[field] is None:
                data[field] = ''
        if data.get('user') is None:
            data['user'] = 0
        return data


class CustomerProfileListSerializer(serializers.ModelSerializer):
    """
    Serializer for listing customer profiles.
    Uses uploaded_at instead of created_at.
    """
    username = serializers.CharField(source='user.username', read_only=True)
    type = serializers.CharField(source='user.type', read_only=True)
    uploaded_at = serializers.DateTimeField(source='created_at', read_only=True)

    class Meta:
        model = Profile
        fields = ['user', 'username', 'first_name', 'last_name', 'file', 
                 'uploaded_at', 'type']


class ProfileUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating profile information.
    Handles both profile and user email updates.
    """
    email = serializers.EmailField(required=False)

    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'location', 'tel', 'description', 
                 'working_hours', 'email']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        for field in ['first_name', 'last_name', 'location', 'tel', 'description', 'working_hours']:
            if data[field] is None:
                data[field] = ''
        return data

    def update(self, instance, validated_data):
        """
        Updates profile and user email if provided.
        """
        email = validated_data.pop('email', None)
        
        # Update profile fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        # Update user email if provided
        if email:
            instance.user.email = email
            instance.user.save()
        
        return instance
