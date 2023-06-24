import os

DATABASES = {
    "default": {
        "ENGINE": "django.contrib.gis.db.backends.postgis",
        "NAME": os.environ.get("PGDATABASE", "opentoilet"),
        "USER": os.environ.get("PGUSER", "opentoilet"),
        "HOST": os.environ.get("PGHOST", "localhost"),
        "PASSWORD": os.environ.get("PGPASSWORD", ""),
        "PORT": os.environ.get("PGPORT", 5432),
    }
}
