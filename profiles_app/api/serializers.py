from rest_framework import serializers
from ..models import Profile
from auth_app.models import CustomUser


class ProfileSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.id')
    username = serializers.ReadOnlyField(source='user.username')
    email = serializers.ReadOnlyField(source='user.email')
    type = serializers.ReadOnlyField(source='user.type')

    class Meta:
        model = Profile
        fields = [
            'user', 'username', 'first_name', 'last_name', 'file',
            'location', 'tel', 'description', 'working_hours',
            'type', 'email', 'created_at'
        ]
        read_only_fields = ['user', 'username', 'email', 'type', 'created_at']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        for field in ['first_name', 'last_name', 'location', 'tel', 'description', 'working_hours']:
            if data[field] is None:
                data[field] = ''
        if data.get('user') is None:
            data['user'] = 0
        return data


class ProfileListSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.id')
    username = serializers.ReadOnlyField(source='user.username')
    type = serializers.ReadOnlyField(source='user.type')

    class Meta:
        model = Profile
        fields = [
            'user', 'username', 'first_name', 'last_name', 'file',
            'location', 'tel', 'description', 'working_hours', 'type'
        ]
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
    user = serializers.ReadOnlyField(source='user.id')
    username = serializers.ReadOnlyField(source='user.username')
    type = serializers.ReadOnlyField(source='user.type')
    uploaded_at = serializers.ReadOnlyField(source='created_at')

    class Meta:
        model = Profile
        fields = [
            'user', 'username', 'first_name', 'last_name', 'file', 'uploaded_at', 'type'
        ]
        read_only_fields = ['user', 'username', 'type', 'uploaded_at']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        for field in ['first_name', 'last_name']:
            if data[field] is None:
                data[field] = ''
        if data.get('user') is None:
            data['user'] = 0
        return data


class ProfileUpdateSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=False)

    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'location', 'tel', 'description', 'working_hours', 'email']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        for field in ['first_name', 'last_name', 'location', 'tel', 'description', 'working_hours']:
            if data[field] is None:
                data[field] = ''
        return data

    def update(self, instance, validated_data):
        email = validated_data.pop('email', None)
        if email:
            instance.user.email = email
            instance.user.save()
        return super().update(instance, validated_data)
