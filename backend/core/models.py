from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

# -----------------------------
# CHOICES
# -----------------------------

ROLE_CHOICES = [
    ("superadmin", "Super Admin"),
    ("director", "Director"),
    ("assistant", "Assistant"),
    ("agent", "Agent"),
    ("owner", "Owner"),
]

PLAN_CHOICES = [
    ("starter", "Starter"),
    ("pro", "Pro"),
    ("enterprise", "Enterprise"),
]

PROPERTY_TYPE_CHOICES = [
    ("appartement", "Appartement"),
    ("villa", "Villa"),
    ("maison", "Maison"),
    ("terrain", "Terrain"),
    ("ferme_villa", "Ferme avec villa"),
    ("local_commercial", "Local commercial"),
    ("bureau", "Bureau"),
    ("duplex", "Duplex"),
    ("riad", "Riad / Maison d’hôtes"),
    ("autre", "Autre"),
]

OPERATION_CHOICES = [
    ("location_longue", "Location longue durée"),
    ("location_moyenne", "Location moyenne durée"),
    ("location_courte", "Location courte durée"),
    ("vente", "Vente"),
    ("colocation", "Colocation"),
]

PROPERTY_STATUS_CHOICES = [
    ("disponible", "Disponible"),
    ("occupe", "Occupé"),
    ("loue", "Loué"),
    ("vendu", "Vendu"),
    ("negociation", "En cours de négociation"),
    ("renovation", "En rénovation"),
    ("reserve", "Réservé"),
]

# -----------------------------
# MODELS
# -----------------------------

class Agency(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField(blank=True, null=True)
    plan = models.CharField(max_length=50, choices=PLAN_CHOICES, default="starter")
    subscription_expires = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class User(AbstractUser):
    role = models.CharField(max_length=32, choices=ROLE_CHOICES, default="agent")
    agency = models.ForeignKey(Agency, null=True, blank=True, on_delete=models.SET_NULL, related_name="users")
    phone = models.CharField(max_length=30, blank=True, null=True)


class SoftDeleteModel(models.Model):
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        abstract = True

    def soft_delete(self):
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save()

    def restore(self):
        self.is_deleted = False
        self.deleted_at = None
        self.save()


class Owner(SoftDeleteModel):
    name = models.CharField(max_length=255)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=50, blank=True, null=True)
    id_document = models.FileField(upload_to="owners/docs/", null=True, blank=True)
    agency = models.ForeignKey(Agency, on_delete=models.CASCADE, related_name="owners")

    def __str__(self):
        return self.name


class Property(SoftDeleteModel):
    agency = models.ForeignKey(Agency, on_delete=models.CASCADE, related_name="properties")

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    property_type = models.CharField(max_length=32, choices=PROPERTY_TYPE_CHOICES)
    operation_type = models.CharField(max_length=32, choices=OPERATION_CHOICES)

    status = models.CharField(max_length=32, choices=PROPERTY_STATUS_CHOICES, default="disponible")

    address = models.CharField(max_length=512)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

    price = models.DecimalField(max_digits=12, decimal_places=2)
    area = models.FloatField(null=True, blank=True)

    # caractéristiques détaillées
    meuble = models.BooleanField(default=False)
    chambres = models.IntegerField(null=True, blank=True)
    salles_bain = models.IntegerField(null=True, blank=True)
    etage = models.IntegerField(null=True, blank=True)
    ascenseur = models.BooleanField(default=False)
    balcon = models.BooleanField(default=False)
    terrasse = models.BooleanField(default=False)
    orientation = models.CharField(max_length=50, null=True, blank=True)
    climatisation = models.BooleanField(default=False)
    piscine = models.BooleanField(default=False)
    parking = models.BooleanField(default=False)

    owner = models.ForeignKey(Owner, on_delete=models.SET_NULL, null=True, related_name="properties")
    agents = models.ManyToManyField("core.User", blank=True, related_name="assigned_properties")

    created_by = models.ForeignKey("core.User", null=True, blank=True, on_delete=models.SET_NULL, related_name="created_properties")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.address}"


class Document(SoftDeleteModel):
    DOC_TYPE = [
        ("mandate", "Mandate"),
        ("id", "ID"),
        ("contract", "Contract"),
        ("inventory", "Inventory"),
        ("other", "Other"),
    ]

    agency = models.ForeignKey(Agency, on_delete=models.CASCADE, related_name="documents")
    property = models.ForeignKey(Property, null=True, blank=True, on_delete=models.CASCADE, related_name="documents")
    owner = models.ForeignKey(Owner, null=True, blank=True, on_delete=models.CASCADE, related_name="documents")
    uploaded_by = models.ForeignKey("core.User", null=True, blank=True, on_delete=models.SET_NULL, related_name="uploaded_documents")

    doc_type = models.CharField(max_length=64, choices=DOC_TYPE, default="other")
    file = models.FileField(upload_to="documents/")
    created_at = models.DateTimeField(auto_now_add=True)


class Client(SoftDeleteModel):
    agency = models.ForeignKey(Agency, on_delete=models.CASCADE, related_name="clients")

    name = models.CharField(max_length=255)
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=50, null=True, blank=True)

    budget = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    criteria = models.JSONField(null=True, blank=True)

    assigned_agent = models.ForeignKey("core.User", null=True, blank=True, on_delete=models.SET_NULL, related_name="clients")
    interested_properties = models.ManyToManyField(Property, blank=True, related_name="interested_clients")

    created_at = models.DateTimeField(auto_now_add=True)


class Visit(SoftDeleteModel):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name="visits")
    client = models.ForeignForeignKey(Client, on_delete=models.CASCADE, related_name="visits")
    agent = models.ForeignKey("core.User", on_delete=models.SET_NULL, null=True, related_name="visits")

    scheduled_at = models.DateTimeField()
    status = models.CharField(max_length=32, default="scheduled")
    report = models.TextField(blank=True)
    photos = models.JSONField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)


class Claim(SoftDeleteModel):
    property = models.ForeignKey(Property, null=True, blank=True, on_delete=models.SET_NULL, related_name="claims")
    client = models.ForeignKey(Client, null=True, blank=True, on_delete=models.SET_NULL)
    agent = models.ForeignKey("core.User", null=True, blank=True, on_delete=models.SET_NULL, related_name="claims")

    description = models.TextField()
    status = models.CharField(max_length=32, default="open")
    reminder_sent = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)


class FinanceEntry(SoftDeleteModel):
    ENTRY_TYPE = [
        ("income", "Income"),
        ("expense", "Expense"),
        ("commission", "Commission"),
    ]

    agency = models.ForeignKey(Agency, on_delete=models.CASCADE, related_name="finance_entries")
    property = models.ForeignKey(Property, null=True, blank=True, on_delete=models.SET_NULL, related_name="finance_entries")
    agent = models.ForeignKey("core.User", null=True, blank=True, on_delete=models.SET_NULL, related_name="finance_entries")

    entry_type = models.CharField(max_length=32, choices=ENTRY_TYPE)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    description = models.TextField(blank=True)
    date = models.DateField(default=timezone.now)

    created_by = models.ForeignKey("core.User", null=True, blank=True, on_delete=models.SET_NULL, related_name="created_finances")
    created_at = models.DateTimeField(auto_now_add=True)
