"""Run: python manage.py check_database  -> shows that the system is connected to MySQL and what is stored."""
from django.core.management.base import BaseCommand
from django.db import connection
from django.db.migrations.executor import MigrationExecutor

TABLES = [("auth_user", "Login accounts"), ("main_resident", "Residents"), ("main_staffprofile", "Staff sign-ups"),
          ("main_documenttype", "Document types"), ("main_documentrequest", "Document requests")]


class Command(BaseCommand):
    help = "Check the MySQL connection and show how many records each table has"
    requires_system_checks = []   # so a wrong password shows a friendly message, not a crash

    def handle(self, *args, **opts):
        try:
            with connection.cursor() as c:
                c.execute("SELECT VERSION(), DATABASE()")
                version, db = c.fetchone()
                self.stdout.write(self.style.SUCCESS(f"Connected to MySQL {version}, database '{db}'"))
                for table, label in TABLES:
                    try:
                        c.execute(f"SELECT COUNT(*) FROM {table}")
                        self.stdout.write(f"  {label:<20} {c.fetchone()[0]} record(s)   [{table}]")
                    except Exception:
                        self.stdout.write(self.style.WARNING(f"  {label:<20} table missing -> run: python manage.py migrate"))
            pending = MigrationExecutor(connection).migration_plan(
                MigrationExecutor(connection).loader.graph.leaf_nodes())
            if pending:
                self.stdout.write(self.style.ERROR(
                    f"\n{len(pending)} update(s) not applied to the database yet. Run:  python manage.py migrate"))
            else:
                self.stdout.write(self.style.SUCCESS("Database is up to date."))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Could not connect to MySQL: {e}"))
            self.stdout.write("Check: 1) MySQL is running  2) the database exists (CREATE DATABASE barangay_db ...)  "
                              "3) user/password in barangay/settings.py")
