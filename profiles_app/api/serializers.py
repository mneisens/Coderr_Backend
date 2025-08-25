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


class ProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'location', 'tel', 'description', 'working_hours']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        for field in ['first_name', 'last_name', 'location', 'tel', 'description', 'working_hours']:
            if data[field] is None:
                data[field] = ''
        return data
