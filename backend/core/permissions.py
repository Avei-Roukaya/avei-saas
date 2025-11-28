from rest_framework import permissions

# -------------------------------------------------------
# PERMISSION : SUPER ADMIN
# -------------------------------------------------------

class IsSuperAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            request.user.role == "superadmin"
        )


# -------------------------------------------------------
# PERMISSION : DIRECTEUR D’AGENCE
# -------------------------------------------------------

class IsDirectorOfAgency(permissions.BasePermission):
    """
    Le directeur peut accéder uniquement aux données
    de sa propre agence.
    """
    def has_object_permission(self, request, view, obj):
        return (
            request.user.is_authenticated and
            request.user.role == "director" and
            request.user.agency == obj.agency
        )


# -------------------------------------------------------
# PERMISSION : MÊME AGENCE
# -------------------------------------------------------

class IsSameAgency(permissions.BasePermission):
    """
    Bloque l’accès aux données d’autres agences.
    """
    def has_object_permission(self, request, view, obj):
        try:
            return (
                request.user.is_authenticated and
                obj.agency == request.user.agency
            )
        except:
            return False


# -------------------------------------------------------
# PERMISSION : FINANCES
# -------------------------------------------------------

class CanViewFinance(permissions.BasePermission):
    """
    Super admin NE VOIT PAS les finances des agences.
    Directeur OUI.  
    Agent : finance du bien qu’il gère ou qu’il a créé.
    """
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            request.user.role in ("director", "agent")
        )

    def has_object_permission(self, request, view, obj):
        user = request.user

        if user.role == "director":
            return obj.agency == user.agency

        if user.role == "agent":
            return obj.agent == user

        return False
