from rest_framework import serializers
from .models import Host, Meeting
from .id_card_generator import *

# class HostSerializer(serializers.Serializer):

class HostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Host
        fields = '__all__'

class MeetingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meeting
        fields = '__all__'




class VisitorIDCardSerializer(serializers.Serializer):
    visitor_name = serializers.CharField(max_length=100)
    visitor_image_path = serializers.CharField()

    def create(self, validated_data):
        visitor_name = validated_data['visitor_name']
        visitor_image_path = validated_data['visitor_image_path']

        try:
            id_card_buffer = VisitorIDCardGenerator.generate(visitor_name, visitor_image_path)
        except Exception as e:
            raise serializers.ValidationError(str(e))

        return {'id_card': id_card_buffer.getvalue()}




# class VisitorIDCardSerializer(serializers.Serializer):
#     visitor_name = serializers.CharField(max_length=100)
#     visitor_image_path = serializers.CharField()

#     def create(self, validated_data):
#         """
#         Generate visitor ID card.
#         """
#         visitor_name = validated_data['visitor_name']
#         visitor_image_path = validated_data['visitor_image_path']

#         try:
#             id_card_buffer = VisitorIDCardGenerator.generate(visitor_name, visitor_image_path)
#         except Exception as e:
#             raise serializers.ValidationError(str(e))

#         return {'id_card': id_card_buffer.getvalue()}


# visitors/serializers.py
from rest_framework import serializers
from .models import Visitor

class VisitorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Visitor
        fields = '__all__'
