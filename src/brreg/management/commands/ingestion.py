from typing import Any, Unpack

from django.core.management.base import BaseCommand, CommandParser

from ...ingestion.main import ingest


class Command(BaseCommand):
    help = "Import data from external sources"

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument("--source", type=str, required=True, help="Data source to import from")
        parser.add_argument("--limit", type=int, default=100, help="Limit number of records to import")

    def handle(self, *args: list[Any], **options: Unpack[dict[str, Any]]) -> None:
        self.stdout.write("Importing data...")

        ingest(**options)
        self.stdout.write(self.style.SUCCESS("Data import complete."))
