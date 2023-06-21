"""
Serilaizer for Motorist Api.
"""
from rest_framework import serializers

from core.models import Vehicle

class VehicleSerializer(serializers.ModelSerializer):
    """Serializer for vehicles."""

    class Meta:
        model = Vehicle
        fields = [
            'id',
            'vehicle_type',
            'last_visit_date',
            'vidange_oil',
            'last_vidange_oil_date',
            'vidange_duration',
            'kilometrage'
        ]
        read_only_fields = ['id']

class VehicleDetailSerializer(VehicleSerializer):
    """Serializer for vehicle detail view."""

    class Meta(VehicleSerializer.Meta):
        fields = VehicleSerializer.Meta.fields