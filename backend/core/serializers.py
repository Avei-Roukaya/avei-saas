from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import (
    Agency, Owner, Property, Document, Client,
    Visit, Claim, FinanceEntry
)

User = get_user_model()

# -----------------------------
# UTILISATEURS
# -----------------------------

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ("password",)

# -----------------------------
# AGENCE
# -----------------------------

class AgencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Agency
        fields = "__all__"

# -----------------------------
# PROPRIÉTAIRE
# -----------------------------

class OwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Owner
        fields = "__all__"

# -----------------------------
# BIEN IMMOBILIER
# -----------------------------

class PropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = "__all__"
        read_only_fields = ("created_by", "created_at")

# -----------------------------
# DOCUMENTS
# -----------------------------

class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = "__all__"

# -----------------------------
# CLIENTS
# -----------------------------

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = "__all__"

# -----------------------------
# VISITES
# -----------------------------

class VisitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Visit
        fields = "__all__"

# -----------------------------
# RÉCLAMATIONS
# -----------------------------

class ClaimSerializer(serializers.ModelSerializer):
    class Meta:
        model = Claim
        fields = "__all__"

# -----------------------------
# FINANCES
# -----------------------------

class FinanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = FinanceEntry
        fields = "__all__"
