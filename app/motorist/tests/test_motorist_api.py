"""
Tests for motorist APIs.
"""
from datetime import datetime

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Vehicle

from motorist.serializers import (
    VehicleSerializer,
    VehicleDetailSerializer,
)

VEHICLES_URL = reverse('motorist:vehicle-list')

def detail_url(vehicle_id):
    """Create and return a vehicle detail URL."""
    return reverse('motorist:vehicle-detail', args=[vehicle_id])

def create_vehicle(user, **params):
    """Create and return a sample vehicle."""
    defaults = {
        'vehicle_type': 'berlin',
        'last_visit_date': datetime.now().date(),
        'vidange_oil': "EMS",
        'last_vidange_oil_date' : datetime.now().date(),
        'vidange_duration' : 25,
        'kilometrage' : 24
    }
    defaults.update(params)

    vehicle = Vehicle.objects.create(user=user, **defaults)
    return vehicle

class PublicVehicleAPITests(TestCase):
    """Test unauthenticated API requests."""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test auth is required to call API."""
        res = self.client.get(VEHICLES_URL)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

class PrivateVehicleApiTests(TestCase):
    """Test authenticated API requests."""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'motorist@example.com',
            'motorit-pass-123',
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_vehicles(self):
        """Test retrieving a list of vehicles."""
        create_vehicle(user=self.user)
        create_vehicle(user=self.user)

        res = self.client.get(VEHICLES_URL)

        vehicles = Vehicle.objects.all().order_by("-id")
        serializer = VehicleSerializer(vehicles, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_vehicle_list_limited_to_user(self):
        """Test list of vehicles is limited to authenticated user."""
        other_user = get_user_model().objects.create_user(
            'other@example.com',
            'password123',
        )
        create_vehicle(user=other_user)
        create_vehicle(user=other_user)

        res = self.client.get(VEHICLES_URL)

        vehicles = Vehicle.objects.filter(user=self.user)
        serializer = VehicleSerializer(vehicles, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_get_vehicle_detail(self):
        """Test get vehicle detail."""
        vehicle = create_vehicle(user=self.user)

        url = detail_url(vehicle.id)
        res = self.client.get(url)

        serializer = VehicleDetailSerializer(vehicle)
        self.assertEqual(res.data, serializer.data)
