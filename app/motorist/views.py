"""
views for vehicle APIs.
"""
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Vehicle
from motorist import serializers


class VehicleViewSet(viewsets.ModelViewSet):
    """View for manage motorist APIs."""
    serializer_class = serializers.VehicleDetailSerializer
    queryset = Vehicle.objects.all()
    authentication_class = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Retrieve vehicles for authenticated user."""
        return self.queryset.filter(user=self.request.user).order_by('-id')

    def get_serializer_class(self):
        """Return the serializer class for request."""
        if self.action == 'list':
            return serializers.VehicleSerializer
        return self.serializer_class