"""SAFETY CHECK: this system must run on MySQL. If the database setting is changed to anything else
(for example SQLite), Django stops with an error when you run runserver / migrate / check."""
from django.core import checks
from django.db import connection


@checks.register()
def mysql_only(app_configs, **kwargs):
    if connection.vendor != "mysql":
        return [checks.Error(
            f"This project must use MySQL, but the database is '{connection.vendor}'.",
            hint="Fix the DATABASES section in barangay/settings.py.", id="main.E001")]
    return []
