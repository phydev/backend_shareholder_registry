import uuid

from django.db import models


class LegalForm(models.Model):
    """
    LegalForm entity, used to store legal form details.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    code = models.CharField(max_length=20, unique=True, null=True, help_text="Koden for organisasjonsform")
    description = models.CharField(max_length=255, null=True,help_text="Beskrivelsen for organisasjonsform")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "legal_form"

    def __str__(self) -> str:
        return f"{self.code} {self.description}"
