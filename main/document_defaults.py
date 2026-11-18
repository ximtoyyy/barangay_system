"""THE LIST OF DOCUMENTS RESIDENTS CAN REQUEST, WITH A LOW DEFAULT FEE (in pesos).
These fees are estimates. Confirm them with your barangay's ordinance, then change any fee in
/admin/ > Document types (no code needed). Fee 0 = free.
To add or rename a document, edit the list below and run: python manage.py seed_documents
(seed_documents only adds missing documents. It never changes a fee you already set.)
"""

DEFAULT_DOCUMENTS = [
    # (name, fee)
    ("Barangay Clearance", 50),
    ("Barangay Certificate of Residency", 30),
    ("Certificate of Indigency", 0),
    ("Certificate of Low Income", 0),
    ("Certificate of No Income", 0),
    ("Certificate of Good Moral Character", 50),
    ("Certificate of First-Time Job Seeker", 0),      # free by law (RA 11261)
    ("Barangay Business Clearance", 200),
    ("Certificate of No Business", 50),
    ("Certificate of Solo Parent", 30),
    ("Certificate of Relationship", 30),
    ("Certificate of Actual Residency", 30),
    ("Certificate of House Ownership/Occupancy", 50),
    ("Certificate of Living Together", 50),
    ("Certificate of Death (Barangay Certification)", 30),
    ("Certificate of Birth (Barangay Certification)", 30),
    ("Certificate of Guardianship", 50),
    ("Certificate of Unemployment", 30),
    ("Certificate of Lot Ownership/Occupancy", 50),
    ("Barangay Certification for Scholarship", 0),
]

# names used by the older version of this system -> renamed (existing requests stay linked)
RENAMED = {
    "Certificate of Residency": "Barangay Certificate of Residency",
    "Business Clearance": "Barangay Business Clearance",
}


def add_default_documents(DocumentType, fill_zero_fees=False):
    """Add any missing document. Returns a list of (name, was_added).
    fill_zero_fees=True (used once by a migration) also gives the default fee to documents still at 0."""
    for old, new in RENAMED.items():
        if DocumentType.objects.filter(name=old).exists() and not DocumentType.objects.filter(name=new).exists():
            DocumentType.objects.filter(name=old).update(name=new)
    result = []
    for name, fee in DEFAULT_DOCUMENTS:
        obj, created = DocumentType.objects.get_or_create(name=name, defaults={"fee": fee})
        if not created and fill_zero_fees and obj.fee == 0 and fee > 0:
            obj.fee = fee
            obj.save(update_fields=["fee"])
        result.append((name, created))
    return result
