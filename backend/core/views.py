from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from django.contrib.auth import get_user_model

from .models import (
    Agency, Owner, Property, Document, Client,
    Visit, Claim, FinanceEntry
)
from .serializers import (
    AgencySerializer, OwnerSerializer, PropertySerializer, DocumentSerializer,
    ClientSerializer, VisitSerializer, ClaimSerializer, FinanceSerializer,
    UserSerializer
)
from .permissions import (
    IsSuperAdmin, IsDirectorOfAgency, IsSameAgency, CanViewFinance
)

User = get_user_model()

# ----------------------------------------------------------
# AGENCES
# ----------------------------------------------------------

class AgencyViewSet(viewsets.ModelViewSet):
    queryset = Agency.objects.all()
    serializer_class = AgencySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == "superadmin":
            return Agency.objects.all()
        return Agency.objects.filter(id=user.agency_id)


# ----------------------------------------------------------
# UTILISATEURS
# ----------------------------------------------------------

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        if user.role == "superadmin":
            return User.objects.all()

        if user.agency:
            return User.objects.filter(agency=user.agency)

        return User.objects.none()


# ----------------------------------------------------------
# PROPRIÉTAIRES
# ----------------------------------------------------------

class OwnerViewSet(viewsets.ModelViewSet):
    queryset = Owner.objects.filter(is_deleted=False)
    serializer_class = OwnerSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        if user.role == "superadmin":
            return Owner.objects.none()

        return Owner.objects.filter(agency=user.agency, is_deleted=False)


    def perform_create(self, serializer):
        serializer.save(agency=self.request.user.agency)


# ----------------------------------------------------------
# BIENS IMMOBILIERS
# ----------------------------------------------------------

class PropertyViewSet(viewsets.ModelViewSet):
    queryset = Property.objects.filter(is_deleted=False)
    serializer_class = PropertySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        qs = Property.objects.filter(is_deleted=False)

        if user.role == "superadmin":
            return Property.objects.none()     # superadmin ne voit pas les biens internes

        if user.role == "agent":
            return qs.filter(
                Q(agency=user.agency) &
                (Q(created_by=user) | Q(agents=user))
            )

        if user.role in ("director", "assistant"):
            return qs.filter(agency=user.agency)

        return Property.objects.none()

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(
            agency=user.agency,
            created_by=user
        )


# ----------------------------------------------------------
# DOCUMENTS
# ----------------------------------------------------------

class DocumentViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.filter(is_deleted=False)
    serializer_class = DocumentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        if user.role == "superadmin":
            return Document.objects.none()

        return Document.objects.filter(agency=user.agency, is_deleted=False)


# ----------------------------------------------------------
# CLIENTS
# ----------------------------------------------------------

class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.filter(is_deleted=False)
    serializer_class = ClientSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        qs = Client.objects.filter(is_deleted=False)

        if user.role == "superadmin":
            return qs.none()

        if user.role == "agent":
            return qs.filter(
                Q(agency=user.agency) &
                (Q(assigned_agent=user) | Q(created_at__isnull=False))
            )

        return qs.filter(agency=user.agency)

    def perform_create(self, serializer):
        serializer.save(agency=self.request.user.agency)


# ----------------------------------------------------------
# VISITES
# ----------------------------------------------------------

class VisitViewSet(viewsets.ModelViewSet):
    queryset = Visit.objects.filter(is_deleted=False)
    serializer_class = VisitSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        qs = Visit.objects.filter(is_deleted=False)

        if user.role == "superadmin":
            return qs.none()

        if user.role == "agent":
            return qs.filter(agent=user)

        return qs.filter(property__agency=user.agency)


# ----------------------------------------------------------
# RÉCLAMATIONS
# ----------------------------------------------------------

class ClaimViewSet(viewsets.ModelViewSet):
    queryset = Claim.objects.filter(is_deleted=False)
    serializer_class = ClaimSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        qs = Claim.objects.filter(is_deleted=False)

        if user.role == "superadmin":
            return qs.none()

        if user.role == "agent":
            return qs.filter(agent=user)

        return qs.filter(property__agency=user.agency)


# ----------------------------------------------------------
# FINANCES
# ----------------------------------------------------------

class FinanceViewSet(viewsets.ModelViewSet):
    queryset = FinanceEntry.objects.filter(is_deleted=False)
    serializer_class = FinanceSerializer
    permission_classes = [IsAuthenticated, CanViewFinance]

    def get_queryset(self):
        user = self.request.user
        qs = FinanceEntry.objects.filter(is_deleted=False)

        if user.role == "director":
            return qs.filter(agency=user.agency)

        if user.role == "agent":
            return qs.filter(agent=user)

        return qs.none()

    def perform_create(self, serializer):
        serializer.save(
            agency=self.request.user.agency,
            created_by=self.request.user
        )
