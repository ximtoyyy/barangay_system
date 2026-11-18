"""Makes the barangay settings (name, logos...) available in every template as {{ barangay_setting }}."""
from .models import BarangaySetting


def barangay(request):
    return {"barangay_setting": BarangaySetting.load()}
