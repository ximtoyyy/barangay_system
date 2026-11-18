"""WHICH CERTIFICATE TEMPLATE PRINTS FOR WHICH DOCUMENT.
Each document name -> its own file in main/templates/certificates/. Any other document uses generic.html.
To add a new certificate: create the template file there and add one line below."""

CERTIFICATE_TEMPLATES = {
    "Barangay Clearance": "barangay_clearance",
    "Barangay Certificate of Residency": "certificate_of_residency",
    "Certificate of Indigency": "certificate_of_indigency",
    "Certificate of Low Income": "certificate_of_low_income",
    "Certificate of No Income": "certificate_of_no_income",
    "Certificate of Good Moral Character": "certificate_of_good_moral_character",
    "Certificate of First-Time Job Seeker": "certificate_of_first_time_job_seeker",
    "Barangay Business Clearance": "barangay_business_clearance",
    "Certificate of No Business": "certificate_of_no_business",
    "Certificate of Solo Parent": "certificate_of_solo_parent",
    "Certificate of Relationship": "certificate_of_relationship",
    "Certificate of Actual Residency": "certificate_of_actual_residency",
    "Certificate of House Ownership/Occupancy": "certificate_of_house_ownership_occupancy",
    "Certificate of Living Together": "certificate_of_living_together",
    "Certificate of Death (Barangay Certification)": "certificate_of_death",
    "Certificate of Birth (Barangay Certification)": "certificate_of_birth",
    "Certificate of Guardianship": "certificate_of_guardianship",
    "Certificate of Unemployment": "certificate_of_unemployment",
    "Certificate of Lot Ownership/Occupancy": "certificate_of_lot_ownership_occupancy",
    "Barangay Certification for Scholarship": "barangay_certification_for_scholarship",
}


def certificate_template(document_name):
    return f"certificates/{CERTIFICATE_TEMPLATES.get(document_name, 'generic')}.html"
