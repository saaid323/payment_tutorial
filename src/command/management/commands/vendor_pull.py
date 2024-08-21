from typing import Any
from django.core.management import BaseCommand
import helper
from django.conf import settings


VENDOR_STATICFILES = {
    "flowbite.min.css": "https://cdnjs.cloudflare.com/ajax/libs/flowbite/2.3.0/flowbite.min.css",
    "flowbite.min.js": "https://cdnjs.cloudflare.com/ajax/libs/flowbite/2.3.0/flowbite.min.js",
    "flowbite.min.js.map": "https://cdnjs.cloudflare.com/ajax/libs/flowbite/2.3.0/flowbite.min.js.map"
}

STATICFILES_VENDOR_DIR = getattr(settings, 'STATICFILES_VENDOR_DIR')
STATICFILES_VENDOR_DIR.mkdir(exist_ok=True, parents=True)

class Command(BaseCommand):

    def handle(self, *args: Any, **options: Any):
        self.stdout.write("Downloading vendor static")
        completed = []
        for name, url in VENDOR_STATICFILES.items():
            out_path = STATICFILES_VENDOR_DIR / name
            dl_success = helper.download_to_local(url, out_path)
            if dl_success:
                completed.append(url)
            else:
                self.stdout.write(self.style.ERROR(f"Failed to download {url}"))
        if set(completed) == set(VENDOR_STATICFILES.values()):
            self.stdout.write(self.style.SUCCESS("Successfully updated all vendor files"))
        else:
            self.stdout.write(self.style.WARNING("Some files were not updates"))
        