from pathlib import Path
from django.core.files import File
from django.db import migrations


def add_default_qr(apps, schema_editor):
    """Put the barangay's QR Ph code (main/static/img/default_qr_ph.png) into Barangay settings.
    Does nothing if a QR was already uploaded, so it never replaces your own upload."""
    Setting = apps.get_model("main", "BarangaySetting")
    setting = Setting.objects.first() or Setting()
    src = Path(__file__).resolve().parent.parent / "static" / "img" / "default_qr_ph.png"
    if setting.qr_image or not src.exists():
        return
    setting.qr_account_name = setting.qr_account_name or "ERNESTO ALMONIA III (MariBank)"
    setting.qr_note = setting.qr_note or "Scan with GCash, Maya or any bank / e-wallet app that supports QR Ph. Type the exact amount."
    with open(src, "rb") as f:
        setting.qr_image.save("qr_ph.png", File(f), save=False)
    setting.save()


class Migration(migrations.Migration):
    dependencies = [("main", "0010_payment_method_qrph_settings_details")]
    operations = [migrations.RunPython(add_default_qr, migrations.RunPython.noop)]
