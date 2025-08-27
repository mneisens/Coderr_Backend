from rest_framework import serializers
from ..models import Offer, OfferDetail
from profiles_app.models import Profile


class OfferDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for OfferDetail objects.
    Used for detailed representation of offer details.
    """
    class Meta:
        model = OfferDetail
        fields = ['id', 'title', 'revisions', 'delivery_time_in_days', 'price', 'features', 'offer_type']


class OfferDetailCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = OfferDetail
        fields = ['title', 'revisions', 'delivery_time_in_days', 'price', 'features', 'offer_type']


class OfferDetailUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating OfferDetail objects.
    Used specifically for PATCH operations on offer details.
    """
    id = serializers.IntegerField(required=False)
    offer_type = serializers.CharField(required=True)

    class Meta:
        model = OfferDetail
        fields = ['id', 'title', 'revisions', 'delivery_time_in_days', 'price', 'features', 'offer_type']

    def validate(self, data):
        """
        Validates that offer_type is provided and valid.
        """
        offer_type = data.get('offer_type')
        if not offer_type:
            raise serializers.ValidationError("Der Typ (offer_type) muss immer mitgegeben werden, um das Detail eindeutig zu identifizieren.")
        
        valid_types = ['basic', 'standard', 'premium']
        if offer_type not in valid_types:
            raise serializers.ValidationError(f"Ungültiger offer_type. Erlaubte Werte: {', '.join(valid_types)}")
        
        return data


class UserDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'username']


class OfferListSerializer(serializers.ModelSerializer):
    """
    Serializer for listing offers.
    Includes basic offer information and user details.
    """
    details = serializers.SerializerMethodField()
    min_price = serializers.ReadOnlyField()
    min_delivery_time = serializers.ReadOnlyField()
    user_details = serializers.SerializerMethodField()

    class Meta:
        model = Offer
        fields = ['id', 'user', 'title', 'image', 'description', 'created_at', 'updated_at',
                  'details', 'min_price', 'min_delivery_time', 'user_details']

    def get_details(self, obj):
        """
        Returns a list of offer detail URLs.
        """
        details = obj.details.all()
        return [{'id': detail.id, 'url': f'/api/offerdetails/{detail.id}/'} for detail in details]

    def get_user_details(self, obj):
        """
        Returns basic user information for the offer creator.
        """
        try:
            profile = Profile.objects.get(user=obj.user)
            return UserDetailsSerializer(profile).data
        except Profile.DoesNotExist:
            return None


class OfferCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating offers.
    Handles nested offer details creation.
    """
    details = OfferDetailCreateSerializer(many=True)

    class Meta:
        model = Offer
        fields = ['title', 'image', 'description', 'details']

    def create(self, validated_data):
        """
        Creates an offer with nested offer details.
        """
        details_data = validated_data.pop('details')
        offer = Offer.objects.create(**validated_data)

        created_details = []
        for detail_data in details_data:
            detail = OfferDetail.objects.create(offer=offer, **detail_data)
            created_details.append(detail)
        offer._created_details = created_details
        return offer

    def to_representation(self, instance):
        """
        Returns the created offer with full details.
        """
        data = super().to_representation(instance)
        response_data = {
            'id': instance.id,
            'title': data.get('title'),
            'image': data.get('image'),
            'description': data.get('description'),
            'details': []
        }
        
        if hasattr(instance, '_created_details'):
            response_data['details'] = OfferDetailSerializer(instance._created_details, many=True).data
        else:
            details = instance.details.all()
            response_data['details'] = OfferDetailSerializer(details, many=True).data
            
        return response_data

    def validate_details(self, value):
        if len(value) != 3:
            raise serializers.ValidationError("Ein Angebot muss genau 3 Details enthalten.")
        return value


class OfferUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating offers.
    Handles nested offer details updates.
    """
    details = OfferDetailUpdateSerializer(many=True, required=False)

    class Meta:
        model = Offer
        fields = ['title', 'image', 'description', 'details']

    def update(self, instance, validated_data):
        """
        Updates an offer and its details.
        """
        details_data = validated_data.pop('details', None)
        instance.title = validated_data.get('title', instance.title)
        instance.image = validated_data.get('image', instance.image)
        instance.description = validated_data.get('description', instance.description)
        instance.save()

        if details_data:
            for detail_data in details_data:
                detail_id = detail_data.get('id')
                offer_type = detail_data.get('offer_type')
                
                if not offer_type:
                    raise serializers.ValidationError("Der Typ (offer_type) muss immer mitgegeben werden, um das Detail eindeutig zu identifizieren.")
                
                if detail_id:
                    try:
                        detail = OfferDetail.objects.get(id=detail_id, offer=instance)
                        for field, value in detail_data.items():
                            if field != 'id' and hasattr(detail, field):
                                setattr(detail, field, value)
                        detail.save()
                    except OfferDetail.DoesNotExist:
                        pass
                else:
                    try:
                        detail = OfferDetail.objects.get(offer=instance, offer_type=offer_type)
                        for field, value in detail_data.items():
                            if field != 'id' and hasattr(detail, field):
                                setattr(detail, field, value)
                        detail.save()
                    except OfferDetail.DoesNotExist:
                        pass

        return instance

    def to_representation(self, instance):
        """
        Returns the updated offer with full details.
        """
        data = super().to_representation(instance)
        response_data = {
            'id': instance.id,
            'title': data.get('title'),
            'image': data.get('image'),
            'description': data.get('description'),
            'details': []
        }
        details = instance.details.all()
        response_data['details'] = OfferDetailSerializer(details, many=True).data
            
        return response_data


class OfferRetrieveSerializer(serializers.ModelSerializer):
    """
    Serializer for retrieving single offers.
    Includes full offer details and metadata.
    """
    details = serializers.SerializerMethodField()
    min_price = serializers.ReadOnlyField()
    min_delivery_time = serializers.ReadOnlyField()

    class Meta:
        model = Offer
        fields = ['id', 'user', 'title', 'image', 'description', 'created_at', 'updated_at',
                  'details', 'min_price', 'min_delivery_time']

    def get_details(self, obj):
        """
        Returns full offer details with complete information.
        """
        details = obj.details.all()
        return OfferDetailSerializer(details, many=True).data
