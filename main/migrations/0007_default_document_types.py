from django.db import migrations
from main.document_defaults import add_default_documents


def add_documents(apps, schema_editor):
    add_default_documents(apps.get_model("main", "DocumentType"))


class Migration(migrations.Migration):
    dependencies = [("main", "0006_documentrequest_handled_by")]
    operations = [migrations.RunPython(add_documents, migrations.RunPython.noop)]
