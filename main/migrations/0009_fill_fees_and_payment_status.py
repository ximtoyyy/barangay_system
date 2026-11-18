from django.db import migrations
from main.document_defaults import add_default_documents


def fill(apps, schema_editor):
    """One time: give documents still at fee 0 their default fee, and set the fee/payment of existing requests."""
    add_default_documents(apps.get_model("main", "DocumentType"), fill_zero_fees=True)
    for r in apps.get_model("main", "DocumentRequest").objects.select_related("document_type"):
        r.fee_charged = r.document_type.fee
        r.payment_status = "free" if r.fee_charged == 0 else "unpaid"
        r.save(update_fields=["fee_charged", "payment_status"])


class Migration(migrations.Migration):
    dependencies = [("main", "0008_documentrequest_fee_charged_documentrequest_paid_at_and_more")]
    operations = [migrations.RunPython(fill, migrations.RunPython.noop)]
