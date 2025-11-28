from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    AgencyViewSet, UserViewSet, OwnerViewSet, PropertyViewSet,
    DocumentViewSet, ClientViewSet, VisitViewSet, ClaimViewSet,
    FinanceViewSet
)

router = DefaultRouter()

# Routes API pour chaque ressource
router.register(r"agencies", AgencyViewSet, basename="agencies")
router.register(r"users", UserViewSet, basename="users")
router.register(r"owners", OwnerViewSet, basename="owners")
router.register(r"properties", PropertyViewSet, basename="properties")
router.register(r"documents", DocumentViewSet, basename="documents")
router.register(r"clients", ClientViewSet, basename="clients")
router.register(r"visits", VisitViewSet, basename="visits")
router.register(r"claims", ClaimViewSet, basename="claims")
router.register(r"finances", FinanceViewSet, basename="finances")

urlpatterns = [
    path("", include(router.urls)),
]
