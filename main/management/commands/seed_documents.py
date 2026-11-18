"""Run: python manage.py seed_documents
Adds any document from main/document_defaults.py that is missing (safe to run many times; never changes existing fees)."""
from django.core.management.base import BaseCommand
from main.document_defaults import add_default_documents
from main.models import DocumentType


class Command(BaseCommand):
    help = "Add the default barangay documents that are missing"

    def handle(self, *args, **opts):
        for name, created in add_default_documents(DocumentType):
            self.stdout.write(f"{'added' if created else 'exists'}: {name}")
