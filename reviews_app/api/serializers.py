from rest_framework import serializers
from ..models import Review
from offers_app.models import Offer


class ReviewSerializer(serializers.ModelSerializer):
    business_user = serializers.SerializerMethodField()

    class Meta:
        model = Review
        fields = ['id', 'reviewer', 'rating', 'description', 'created_at', 'updated_at', 'offer', 'business_user']
        read_only_fields = ['id', 'reviewer', 'created_at', 'updated_at', 'offer']

    def get_business_user(self, obj):
        return obj.offer.user.id


class ReviewUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['rating', 'description']


class ReviewListSerializer(serializers.ModelSerializer):
    business_user = serializers.SerializerMethodField()

    class Meta:
        model = Review
        fields = ['id', 'reviewer', 'rating', 'description', 'created_at', 'updated_at', 'offer', 'business_user']
        read_only_fields = ['id', 'reviewer', 'created_at', 'updated_at', 'offer']

    def get_business_user(self, obj):
        return obj.offer.user.id


class ReviewUpdateOnlySerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['rating', 'description']


class ReviewCreateOnlySerializer(serializers.ModelSerializer):
    business_user = serializers.IntegerField(write_only=True, required=False)
    offer = serializers.PrimaryKeyRelatedField(queryset=Offer.objects.all(), required=False)
    business_user_id = serializers.IntegerField(write_only=True, required=False)

    class Meta:
        model = Review
        fields = ['offer', 'business_user', 'business_user_id', 'rating', 'description']
        extra_kwargs = {
            'rating': {'required': True},
            'description': {'required': True}
        }

    def to_internal_value(self, data):
        data_copy = data.copy()
        
        if 'business_user' in data_copy:
            business_user_id = data_copy.pop('business_user')
            self.context['business_user_id'] = business_user_id
            
        if 'business_user_id' in data_copy:
            business_user_id = data_copy.pop('business_user_id')
            self.context['business_user_id'] = business_user_id
            
        return super().to_internal_value(data_copy)

    def validate(self, data):
        business_user_id = self.context.get('business_user_id')
        
        if not data.get('offer') and business_user_id:
            try:
                offer = Offer.objects.filter(user_id=business_user_id).first()
                if offer:
                    data['offer'] = offer
                else:
                    raise serializers.ValidationError("Kein Angebot für diesen Business User gefunden.")
            except Exception as e:
                raise serializers.ValidationError(f"Ungültiger Business User: {str(e)}")

        if not data.get('offer'):
            raise serializers.ValidationError("Entweder 'offer' oder 'business_user' muss angegeben werden.")

        return data
