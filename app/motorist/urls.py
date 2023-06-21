"""
URL mapping for the motorist app.
"""
from django.urls import(
    path,
    include,
)
from rest_framework.routers import DefaultRouter
from motorist import views

router = DefaultRouter()
router.register('motorist', views.VehicleViewSet)

app_name = 'motorist'

urlpatterns = [
    path('', include(router.urls)),
]