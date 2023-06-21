"""
Tests for models.
"""
from decimal import Decimal
from datetime import datetime

from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models

class ModelTests(TestCase):
    """Test models."""
    def test_create_user_with_email_successful(self):
        """Test creating a user with an email is successful."""
        email = 'test@example.com'
        password = 'testpass123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test email is normalized for new users."""
        sample_emails = [
            ['test1@EXAMPLE.com', 'test1@example.com'],
            ['Test2@Example.com', 'Test2@example.com'],
            ['TEST3@EXAMPLE.COM', 'TEST3@example.com'],
            ['test4@example.COM','test4@example.com'],
        ]
        for email, expected_email in sample_emails:
            user = get_user_model().objects.create_user(email, 'testpass123')
            self.assertEqual(user.email, expected_email)

    def test_new_user_without_email_raises_error(self):
        """Test that creating a user without an email raises a ValueError."""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('', 'testpass123')

    def test_create_superuser(self):
        """Test creating a superuser."""
        user = get_user_model().objects.create_superuser(
            'admin@example.com',
            'adminpass123'
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    # def test_create_motorist(self):
    #     """Test creating a motorist is successful."""
    #     user = get_user_model().objects.create_user(
    #         'test@example.com',
    #         'testpass123',
    #     )
    #     motorist = models.Motorist.objects.create(
    #         user=user,
    #         surname="Motorist",
    #     )

    #     self.assertEqual(str(motorist), motorist.surname)
    #     self.assertTrue(motorist.is_motorist)

    def test_create_vehicle(self):
        """Test creating a vehicle is successful."""
        user = get_user_model().objects.create_user(
            'test@example.com',
            'testpass123',
        )
        vehicle = models.Vehicle.objects.create(
            user=user,
            vehicle_type="Berlin", #this should be a select field
            last_visit_date=datetime.now().date(),
            vidange_oil="EMS",
            last_vidange_oil_date=datetime.now().date(),
            vidange_duration=25,
            kilometrage=24
        )

        self.assertEqual(str(vehicle), vehicle.vehicle_type)