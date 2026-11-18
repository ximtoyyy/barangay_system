"""DJANGO /admin/ SCREEN: which tables the admin can open in /admin/."""
from django.contrib import admin
from .models import Resident, StaffProfile, DocumentType, DocumentRequest, BarangaySetting

@admin.register(Resident)
class ResidentAdmin(admin.ModelAdmin):
    list_display = ("full_name", "user", "approval", "date_registered")
    list_filter = ("approval",)

@admin.register(DocumentRequest)
class DocumentRequestAdmin(admin.ModelAdmin):
    list_display = ("reference_no", "resident", "document_type", "status", "date_requested")
    list_filter = ("status", "document_type")
    search_fields = ("reference_no", "resident__full_name")


@admin.register(StaffProfile)
class StaffProfileAdmin(admin.ModelAdmin):
    list_display = ("full_name", "position", "approval", "date_registered")
    list_filter = ("approval",)


@admin.register(BarangaySetting)
class BarangaySettingAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):        # only one settings row is needed
        return not BarangaySetting.objects.exists()
